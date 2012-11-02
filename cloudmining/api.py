"""The app is a webpy app which calls a fSphinx client and renders
itself accordingly. The default look and feel of the interface can be
set or completely overriden.
"""

__all__ = ['CloudMiningApp']

import web
import os
import sys

from cloudmining.lib import templating, utils, dirmap
from cloudmining.visualization import TagCloud, Counts, Rose

ROOT = os.path.dirname(os.path.realpath(__file__))

COLOR_PALETTE = (
    dict(name='blue', background='#EFF5FF', foreground='#0000CC'),
    dict(name='black', background='#EFEFEF', foreground='#000000'),
    dict(name='green', background='#E1FFDF', foreground='#008000'),
    dict(name='red', background='#FFEFEF', foreground='#EF0000'),
    dict(name='purple', background='#F9F0FD', foreground='#9400D3'),
    dict(name='orange', background='#FBF2EA', foreground='#D2701F'),
    dict(name='pink', background='#FFF2F9',  foreground='#FF1493'),
)

VISUALIZATIONS = ['tag_cloud', 'counts', 'rose']

CONFIG_GLOBALS = (
    'debug', 'db', 'cl', 'sim_cl', 'ui_facets', 'ui_default_hit',
    'ui_sort_by', 'instance_name', 'description', 'view', 'public',
    'simsearch_index', 'results_per_page', 'paging_window_size',
    'ui_facets_dict', 'default_coloring', 'hit_template', 'public_dir',
    'stylesheets', 'javascripts', 'expose', 'visu'
)

MAPPING = (
    '/',
    'cloudmining.app.controllers.base.front_page',
    # search with query parameters
    '/search/?',
    'cloudmining.app.controllers.base.search',
    # search with nice query url
    '/search/(.+)',
    'cloudmining.app.controllers.base.search_url',
    # for ajax facet loading
    '/load_facet/([a-z_-]+)/([a-z_-]+)',
    'cloudmining.app.controllers.base.load_facet',
    # only used in development (make sure you serve statically)
    '/(public|css|js|img)/(.+)',
    'cloudmining.app.controllers.public.public',
)


class CloudMiningApp(web.application, object):
    def __init__(self, cl=None, sim_cl=None, mapping=(), fvars={}, autoreload=None):
        """Creates a CloudMiningApp from a fSphinx client.

        For similarity search a SimClient can also be provided. All the
        remaining options are the same of a webpy app.
        """
        self.set_fsphinx_client(cl)
        self.set_sim_client(sim_cl)
        self.set_ui_instance()

        self.port = 8080
        self.debug = True
        self.flush_cache_on_startup = True
        self.preload_cache_file = ''
        self.template_caching = False
        self.default_coloring = True
        self.expose = False

        self.results_per_page = 10
        self.paging_window_size = 3

        self.javascripts = []
        self.stylesheets = []

        self.view = dirmap.DirectoryMapper(ROOT + '/app/views')
        self.public = dirmap.DirectoryMapper(ROOT + '/public')
        self.hit_template = None

        self.visu = {}
        self.register_visualization(TagCloud, Counts, Rose)

        self.init_webpy_app(mapping, fvars, autoreload)

    def __getattr__(self, name):
        if name in CONFIG_GLOBALS:
            return web.config[name]
        else:
            return web.__dict__[name]

    def __setattr__(self, name, value):
        if name in CONFIG_GLOBALS:
            web.config[name] = value
        else:
            self.__dict__[name] = value

    def init_webpy_app(self, mapping=(), fvars={}, autoreload=None):
        """Initializes webpy app which delegate requests based on path."""
        # the default url mapping
        mapping = mapping + MAPPING
        # not sure why this is needed
        fvars = web.dictadd(locals(), fvars)
        # create webapy app with these settings
        super(CloudMiningApp, self).__init__(mapping, fvars, autoreload)

    def set_fsphinx_client(self, cl):
        """Sets the Sphinx client to be served. Also initializes ui
        elements."""
        self.cl = cl
        # we reset the ui for the facets and other elements
        self.set_ui_facets()
        self.set_ui_default_hit(reset=True)
        self.set_ui_sort_by()

    def set_sim_client(self, sim_cl):
        """Sets the Sphinx client to be served."""
        self.sim_cl = sim_cl

    def set_port(self, port):
        """When using the development server, change the default port (8080)"""
        self.port = port

    def set_ui_sort_by(self, *ui_sort_by):
        """Sets ui element sort by options.

        The options are dictionnaries of the following form:
        dict(key='unique_key', description='sort option description')

        The key must match the sphinx client sort options.
        """
        self.ui_sort_by = ui_sort_by

    def set_ui_instance(self,
        instance_name='Demo', description='This is a demo of CloudMining'):
        """Sets ui element instance name and description."""
        self.instance_name = instance_name
        self.description = description

    def set_ui_facets(self, *ui_facets):
        """Like set_ui_facet but on multiple facets.

        If no parameters is provided set default ui of all facets from
        sphinx client.
        """
        if not ui_facets and self.cl:
            self.ui_facets_dict = {}
            self.ui_facets = []
            for i, f in enumerate(self.cl.facets):
                color = COLOR_PALETTE[i % len(self.cl.facets)]
                ui_facet = web.storage(
                    name=f.name,
                    description=f.name.upper(),
                    color=color,
                    visualization=VISUALIZATIONS[0],
                    available_visualizations=VISUALIZATIONS,
                    collapsed=False
                )
                self.ui_facets.append(ui_facet)
                self.ui_facets_dict[f.name] = ui_facet
        else:
            for ui_facet in ui_facets:
                self.set_ui_facet(**ui_facet)
            
    def set_ui_facet(self, name, description='', color={}, visualization='',
        available_visualizations=(), collapsed=False):
        """Set the ui of a facet given by a name.

        The name must match the facet name in the sphinx client. Other
        parameters will default unless specified:

        :param description: refine by: $description
        :param color: color name or dict
        :param visualization: name of the visualization
        :param available_visualizations: list of visualization names
        :param collapsed: whether the facet starts collapsed
        """
        def get_color_obj(color):
            if isinstance(color, str):
                color = web.listget(
                    [c for c in COLOR_PALETTE if c['name'] is color], 0)
            return color

        ui_facet = self.ui_facets_dict.get(name)
        if ui_facet:
            ui_facet.update(dict((k, v) for k, v in (
                ('description', description),
                ('color', get_color_obj(color)),
                ('visualization', visualization),
                ('available_visualizations', available_visualizations),
                ('collapsed', collapsed)
            ) if v))
            self.ui_facets.remove(ui_facet)
            self.ui_facets.append(ui_facet)
            
    def set_ui_default_hit(self, title_field='', id_field='',
        facet_field_mapping={}, fields_shown=(), reset=False):
        """Set the ui of the default hit look and feel (not overriden by a
        template). We call hit the snippet representing a search result.

        The parameters describe the fields the sphinx client DBFetch and will
        default unless specified:

        :param title_field: what is the title field (default 'title').
        :param id_field: what field correspond to the id (default 'id').
        :param facet_field_mapping: refinable results given by (facet_field, facet_name).
        :param fields_shown: which fields should be shown.
        :param reset: ignore all parameters and set according to sphinx client.
        """
        if reset:
            if self.cl:
                ffm = dict((f.name, f.name) for f in self.cl.facets)
                fs = [f.name for f in self.cl.facets]
            else:
                ffm = {}
                fs = ()
            self.ui_default_hit = web.storage(
                title_field='title',
                id_field='id',
                facet_field_mapping=ffm,
                fields_shown=fs
            )
        else:
            self.ui_default_hit.update(
                dict((k, v) for k, v in locals().items()
                     if v and v not in ['self', 'reset']))

    def set_debug(self, bool):
        """Whether to show debugging django like error."""
        self.debug = bool

    def set_template_caching(self, bool):
        """Whether to use internal webpy template caching."""
        if bool:
            self.view._cache = {}
            self.public._cache = {}
        else:
            self.view._cache = None
            self.public._cache = None
        self.template_caching = bool

    def set_flush_cache_on_startup(self, bool):
        """If a cache is provided by sphinx client, flush it on startup."""
        self.flush_cache_on_startup = bool

    def set_preload_cache_file(self, path):
        """If a cache is provided by sphinx client, preload it on
        startup."""
        self.preload_cache_file = path

    def set_default_coloring(self, bool):
        """Whether to use default coloring."""
        self.default_coloring = bool

    def set_hit_template(self, path):
        """Change default hit template to the one provided."""
        self.hit_template = web.template.Template(open(path).read(), filename=path)

    def override_template(self, path):
        """This will make the search for templates first look into path and
        then to the default path."""
        self.view << path

    def add_template_functions(self, f):
        """Make function available accross all templates."""
        templating.public(f)

    def set_public_dir(self, path='./public'):
        """Where to look for public or static content."""
        self.public.public << path

    def add_stylesheets(self, *path):
        """Add stylesheets to your app.

        The path must be prepended by the path to your public directory ie
        app.add_stylesheets('/public/custom.css').
        """
        utils.add_uniq(self.stylesheets, path)

    def add_javascripts(self, *path):
        """Add javascripts to your app.

        The path must be prepended by the path to your public directory ie
        app.add_stylesheets('/public/js/defaults.js').
        """
        utils.add_uniq(self.javascripts, path)

    def set_application_path(self, path, auto_load_public=False):
        """Sets the root path of your application.

        If the following directories are found:

        /views: will set override template on that directory.
        /public: will set the public directory.
        /data/redis-cache.dat: will set preload cache.

        It will also auto load all files found in /public if auto_load_public
        is set.
        """
        tpl_dir = os.path.join(path, './views')
        if os.path.exists(tpl_dir):
            self.override_template(tpl_dir)
        pub_dir = os.path.join(path, './public')
        if os.path.exists(pub_dir):
            self.set_public_dir(pub_dir)
        che_dir = os.path.join(path, './data/redis-cache.dat')
        if os.path.exists(che_dir):
            self.set_preload_cache_file(che_dir)
        if auto_load_public:
            self.auto_load_public()

    def auto_load_public(self):
        """Anything found in /public will be accessible by your app."""
        ppath = self.public.public._loc[0]
        for f in utils.walkfiles(ppath, '*.css'):
            self.add_stylesheets(os.path.join('/public', f.relpath))
        for f in utils.walkfiles(ppath, '*.js'):
            self.add_javascripts(os.path.join('/public', f.relpath))

    def register_visualization(self, *visu_class):
        """Register a new visualization so it can be added to the list of
        available visualization for the facet."""
        global VISUALIZATIONS
        for v in visu_class:
            v = v(self)
            self.visu[v.name] = v
            if v.name not in VISUALIZATIONS:
                VISUALIZATIONS.append(v.name)

    def run(self, *midleware):
        """After all settings have been set, starts handling requests.

        If called in a CGI or FastCGI context, it will follow that protocol. If
        called from the command line, it will start an HTTP server on the port
        named in the first command line argument, or, if there is no argument,
        on port 8080.

        `middleware` is a list of WSGI middleware which is applied to the
        resulting WSGI funct
        """
        if self.debug:
            print 'Debugger mode on ...'
        if self.template_caching:
            print 'Template caching is turned on ...'
        if self.default_coloring:
            print 'Default CSS coloring ...'
        if getattr(self.cl, 'cache') and self.flush_cache_on_startup:
            print 'Flushing the search cache ...'
            self.cl.cache.Flush()
        if getattr(self.cl, 'cache') and self.preload_cache_file:
            print 'Preloading the search cache with persistent keys ...'
            self.cl.cache.Loads(self.preload_cache_file, -1)

        sys.argv = (None, '0.0.0.0:%s' % self.port)
        web.application.run(self, *midleware)

    @classmethod
    def from_config_dir(cls, path, **opts):
        """Create an app given a path to the sphinx client and sim search
        configuration files.

        |-- config
        |   |-- simsearch_client.py
        |   |-- sphinx_client.py
        |   `-- ...
        """
        from fsphinx import FSphinxClient
        from simsearch import SimClient
        app = CloudMiningApp(**opts)
        if os.path.exists(path):
            for f in utils.walkfiles(path, '*.py'):
                if f.filename == 'sphinx_client.py' and not app.cl:
                    app.set_fsphinx_client(FSphinxClient.FromConfig(f.abspath))
                if f.filename == 'simsearch_client.py' and not app.sim_cl:
                    app.set_sim_client(SimClient.FromConfig(f.abspath))
        return app

    @classmethod
    def from_directory(cls, path, **opts):
        """Create an app assuming the following directory structure.

        |-- config
        |   |-- simsearch_client.py
        |   |-- simsearch_indexer.cfg
        |   |-- sphinx_client.py
        |   `-- sphinx_indexer.cfg
        |-- data
        |   |-- redis-cache.dat
        |   |-- ...
        |   |-- ...
        |   `-- ...
        |-- public
        |   `-- custom.css
        |   `-- ...
        |   `-- ...
        `-- views
            `-- hit.html
            `-- ...
            `-- ...

        public/ holds all the static files and views/ all the templates that
        override the default templates.
        """
        # read configuration files
        app = CloudMiningApp.from_config_dir(os.path.join(path, './config'), **opts)
        # template override, public lookup, search cache
        app.set_application_path(path, auto_load_public=True)
        return app

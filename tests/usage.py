from fsphinx import FSphinxClient
from simsearch import SimClient
from cloudmining import CloudMiningApp

# create a FSphinxClient from the configuration file
cl = FSphinxClient.FromConfig(config_file)

# create similarity search client
sim_cl = SimClient.FromConfig(sim_config_file)

# create a new CloudMining web application
app = CloudMiningApp()

# set the fsphinx client of the webapp
app.set_fsphinx_client(cl)

# same for similarity search
app.set_sim_client(sim_cl)

# request the front page
app.request('/')

# user defaults
# not sure about that ... may be replaced by ui_facets
app.set_user_defaults('config/user_defaults.json')

# override search for templates
app.override_lookup('templates', '.')
# maybe?
app.override_lookup('views', '.')

# override search for css files
app.override_lookup('css', '.')

# override search for img files
app.override_lookup('img', '.')

# integrated web server on port 8080
app.set_port(8080)

# access fsphinx client and change any options
app.config.cl.SetConnectTimeout(2.0)
# maybe?
app.cl.SetConnectTimeout(2.0)

# another example is giving a search caching to cl
app.config.cl.AttachCache(
    RedisCache(db=0, preload='data/redis-cache.dat'))
# maybe?
app.cl.AttachCache(
    RedisCache(db=0, preload='data/redis-cache.dat'))

# if cl has a search cache preload it
app.set_preload_cache_file('data/redis-cache.dat')

# some more options which can be set
app.set_debug_mode(False) # also app.config.debug
app.set_template_caching(False) # also app.config.template_caching
app.config.db.printing = False
app.set_flush_cache_on_startup(True)

# what sorting options are shown (key must match cl sort options)
app.set_ui_sort_by(
    dict(key='pop', description='popularity'),
    dict(key='dat', description='date'),
    dict(key='rat', description='user ratings'),
    dict(key='vot', description='number of votes')
)

# you can reorder the facets here (name must match cl facet names)
app.set_ui_facets(
    dict(name='author', description='AUTHORS', color='blue', visualization='counts'),
    dict(name='year', description='YEAR', color='red'),
    dict(name='keyword', description='KEYWORDS', color='black')
)
# maybe? no because we cannot modify a single value without modifying all of them
app.ui_facets.year = dict(description='YEAR', color='red')
# or?
app.set_ui_facet('year', description='YEAR', color='red')

# this controls the default search result template
# but normally you should write your own overriding the template
app.set_ui_default_hit(
    title_field='title',
    id_field='id',
    facet_fields_mapping=dict(
        author='authors', keyword='plot_keywords'),
    fields_shown = ('authors', 'plot_keywords', 'plot', 'genre')
)

# or setup the look and feel of your own
app.set_hit_template(
    template='./hit.html',
    javascript='./custom.js',
    stylesheet='./custom.css',
    media_directory='./img'
)

# add aditional stylesheets
app.add_stylesheet('./custom.css')

# or aditional javascript files
app.add_javascript('./custom.js')

# or any other header files
app.add_media_directory('./img')

app.register_visualization(
    dict(
        key = 'cumulus',
        description = 'cumulus!',
        setup = lambda x: x(),
        template = './cumulus.html'
        javascript = '',
        stylesheet = ''
    )
    available_in = ['year', 'authors']
)

class Cumulus(Visualization):
    """docstring for Cumulus"""
    def __init__(self, app):
        self.name = 'cumulus'
        self.description = 'cumulus!'
        app.add_javascript('/custom/js/googlejs/cumulus.js')

    def setup(self, facet):
        facet.SetGroupSort('@count asc')

    def render(self, computed_facet):
        return app.custom.cumulus(computed_facet)

app.register_visulization(Cumulus, for_facets=['year', 'authors'])

registered = dict(
    counts_asc={
        'name': 'count_desc',
        'description': 'count desc',
        'compute': lambda(facet): facet.SetGroupSort('@count asc'),
        'template': 'counts.html'
    }
)


app.register_visualization(
    key = 'cumulus',
    description = 'cumulus!',
    setup = lambda x: x(),
    template = './cumulus.html'
    javascript = '',
    stylesheet = ''
)

# add a custom made visualization
app.register_visualization(
    Cumulus,

    facet_names=['year', 'author'])


app.set_ui_facet('year', description='YEAR', color='red')


# setup
# app.set_custom_hit('hit.html')

# app.set_custom_css('custom.css')

# app.set_custom_public_dir('public')

# or set override directoty

# app.add_visulizations ..

class Rose(Visualization):
    def register

    def compute(self, facet):
        facet.compute()

    def render(self, facet):
        self.view.insert(edit, 0, "Hello, World!")



class Visualization(object):
    name = 'hello'
    @classmethod
    def compute(cls, facet):
        return 'yeah cool'

class Treemap(Visualization):
    description = 'Tree Map'
    template_path = '/app/views'
    load_javascript = ''
    @classmethod
    def compute(cls, facet):
        return facet.compute()

app.add_visualization(
    name='treemap', description='', compute='', template_path='', load_javascript=''
)

# if called from the command line will launch testing web server
# otherwise serve as fastcgi
if __name__ == '__main__':
    app.run()

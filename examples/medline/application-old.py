#!/usr/bin/env python
from fsphinx import FSphinxClient
from fsphinx import RedisCache
from simsearch import SimClient
from cloudmining import CloudMiningApp

# create a FSphinxClient from the configuration file
cl = FSphinxClient.FromConfig('config/sphinx_client.py')

# create similarity search client
#sim_cl = SimClient.FromConfig('config/simsearch_cfg.py')

# create a new CloudMining web application
app = CloudMiningApp(autoreload=True)

# set the fsphinx client of the webapp
app.set_fsphinx_client(cl)

# same for similarity search
#app.set_sim_client(sim_cl)

# # override search for templates
# app.override_lookup('templates', '.')
# # maybe?
# app.override_lookup('views', '.')

# # override search for css files
# app.override_lookup('css', '.')

# # override search for img files
# app.override_lookup('img', '.')

# access fsphinx client and change any options
app.cl.SetConnectTimeout(2.0)

# another example is giving a search caching to cl
#app.cl.AttachCache(RedisCache(db=0))

# if cl has a search cache preload it
app.set_preload_cache_file('data/redis-cache.dat')

# some more options which can be set
app.set_debug(True)  # also web.config.debug
app.set_template_caching(False)  # also web.config.template_caching
app.set_flush_cache_on_startup(True)

# what sorting options are shown (key must match cl sort options)
# app.set_ui_sort_by(
#     dict(key='cit', description='number of citations'),
#     dict(key='rel', description='relevance'),
#     dict(key='dat', description='year')
# )

# # you can reorder the facets here (name must match cl facet names)
# app.set_ui_facets(
#     dict(name='author', description='AUTHORS', color='blue', visualization='counts'),
#     dict(name='year', description='YEAR', color='red'),
#     dict(name='keyword', description='KEYWORDS', color='black')
# )

# or change the look and feel of a single facet
# app.set_ui_facet('year', description='YEAR',
#     color='purple', collapsed=True, visualization='counts',
#     available_visualizations=(
#         dict(key='cumulus', description='cumulus!'),
#         dict(key='tag_cloud', description='tag cloud'),
#         dict(key='counts', description='counts'))
#     )

# app.set_ui_facet('year', description='YEAR',
#     color='purple', collapsed=True, visualization='counts',
#     available_visualizations=('tag_cloud', 'counts')
# )

# this controls the default search result template
# but normally you should write your own overriding the template
# app.set_ui_default_hit(
#     title_field='title',
#     id_field='id',
#     facet_field_mapping=dict(
#         author='authors', venue='source_id', year='year'),
#     fields_shown=('author', 'year', 'venue')
# )


import re
import web
def fix_pagination(s):
    if s is None:
        s = ''
    return web.listget(re.findall('^\w?[\d-]+', s), 0)

def fix_author_initials(s):
    s = s.split()
    if len(s) > 1:
        s[-1] = s[-1].upper()
    return ' '.join(s)

app.add_template_functions({
    'fix_pagination': fix_pagination,
    'fix_author_initials': fix_author_initials
})

#app.set_hit_template('./hit.html')

#app.override_template('./views')

#app.set_hit_template('./hit.html')

app.set_public_dir('./public')

app.add_stylesheets('/public/custom.css')

# if called from the command line will start HTTP server
# otherwise it will honor cgi or fastcgi protocol
if __name__ == '__main__':
    app.run()

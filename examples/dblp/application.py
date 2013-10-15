#!/usr/bin/env python
from fsphinx import FSphinxClient
from simsearch import SimClient
from cloudmining import CloudMiningApp

# create a FSphinxClient from the configuration file
cl = FSphinxClient.FromConfig('config/sphinx_client.py')

# create similarity search client
sim_cl = SimClient.FromConfig('config/simsearch_client.py')

# create a new CloudMining web application
app = CloudMiningApp(autoreload=True)

# set the fsphinx client of the webapp
app.set_fsphinx_client(cl)

# same for similarity search
app.set_sim_client(sim_cl)

# if cl has a search cache preload it
app.set_preload_cache_file('data/redis-cache.dat')

# some more options which can be set
app.set_debug(True)  # also web.config.debug
app.set_template_caching(False)  # also web.config.template_caching
app.set_flush_cache_on_startup(True)

# what sorting options are shown (key must match cl sort options)
app.set_ui_sort_by(
    dict(key='cit', description='number of citations'),
    dict(key='rel', description='relevance'),
    dict(key='dat', description='year')
)

# you can reorder the facets and change default look here
# name must match the sphinx client facet names
app.set_ui_facets(
    dict(name='author', description='AUTHORS', color='blue', visualization='counts'),
    dict(name='keyword', description='KEYWORDS', color='black'),
    dict(name='venue', description='VENUE', color='green', visualization='counts'),
    dict(name='year', description='YEAR', color='red', visualization='rose'),
)

# instance name and description which appears in the front page
app.set_ui_instance(
    instance_name='DBLP', 
    description='''<p>Search over 2.4M <strong>computer science publications</strong> from <a href="http://dblp.uni-trier.de/db">DBLP</a>
    enhanced with <a href="http://citeseerx.ist.psu.edu/">CiteSeerX</a>.</p>'''
)

# read templates from this directory first
app.override_template('./views')

# all assets at /public/ will be read here
app.set_public_dir('./public')

# add a custom stylesheet
app.add_stylesheets('/public/custom.css')

# if called from the command line will start HTTP server
# otherwise it will honor cgi or fastcgi protocol
if __name__ == '__main__':
    app.run()

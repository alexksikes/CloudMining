#!/usr/bin/env python
from cloudmining import CloudMiningApp

# assumes a default directory structure
app = CloudMiningApp.from_directory('.', autoreload=True)

# you can reorder the facets and change default look here
# name must match the sphinx client facet names
app.set_ui_facets(
    dict(name='author', visualization='counts'),
    dict(name='journal', color='green', collapsed=True),
    dict(name='mesh', color='black'),
    dict(name='year', visualization='rose'),
)

# some more options which can be set
app.set_debug(True)  # also web.config.debug
app.set_template_caching(False)  # also web.config.template_caching
app.set_flush_cache_on_startup(True)

# instance name and description which appears in the front page
app.set_ui_instance(
    instance_name='MEDLINE', 
    description='''<p>Search over 18M <strong>biomedical articles</strong> from <a href="http://www.ncbi.nlm.nih.gov/pubmed">MEDLINE</a>
    enhanced with citations from <a href="http://www.ncbi.nlm.nih.gov/pmc">Pubmed Central</a>.</p>'''
)

# custom template functions
import lib.templating

# custom search function to handle cite queries
import models.items

# launch default web server
if __name__ == '__main__':
    app.run()

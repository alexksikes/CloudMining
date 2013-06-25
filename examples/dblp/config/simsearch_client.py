import sphinxapi
import fsphinx
import simsearch

# create simsearch client
cl = simsearch.SimClient(
    fsphinx.FSphinxClient.FromConfig('config/sphinx_client.py'), 
    index_path='data/sim-index/',
    max_items=1000
)

# custom sorting function for the search
cl.SetSortMode(sphinxapi.SPH_SORT_EXPR, 'log_score_attr')
    
# custom grouping function for the facets
group_func = 'sum(log_score_attr + 0.1)'
#group_func = 'sum(if (log_score_attr > 1, log_score_attr, 0))'
    
# setup sorting and ordering of each facet 
for f in cl.facets:
    f.SetGroupFunc(group_func)

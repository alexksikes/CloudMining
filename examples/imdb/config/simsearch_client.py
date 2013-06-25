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
# we always make sure highly ranked items with a log score are at the top.
cl.SetSortMode(sphinxapi.SPH_SORT_EXPR, '''
if (log_score_attr > 0 and user_rating_attr > 0.5 and nb_votes_attr > 100,
    log_score_attr,
    (@weight * user_rating_attr * nb_votes_attr) - 1000000000000
)'''
)

# custom grouping function for the facets
# facet terms with a log score are scored otherwise we make sure the terms
# appear but are at the bottom.
group_func = '''
sum(
    if (log_score_attr > 0,
        if (runtime_attr > 45,
            if (nb_votes_attr > 1000,
                if (nb_votes_attr < 10000, nb_votes_attr * user_rating_attr, 10000 * user_rating_attr),
            1000 * user_rating_attr),
        300 * user_rating_attr),
    nb_votes_attr * user_rating_attr / 100000)
)'''

# setup sorting and ordering of each facet
for f in cl.facets:
    # group by a custom function
    f.SetGroupFunc(group_func)

import re
import web

try:
    import simsearch
except ImportError:
    simsearch = None

config = web.config


def get_sphinx_client(query):
    # are we in similarity search mode
    if is_sim_query(query, is_active=True):
        cl = config.sim_cl.Clone()
    else:
        cl = config.cl.Clone()
    return cl
 

def search(query, offset=0, limit=10, sort_by='', user_pref={}):
    # get the sphinx client
    cl = get_sphinx_client(query)
    # set page number and limit
    cl.SetLimits(offset, limit)
    # set the sort by order
    if sort_by:
        cl.SetSortMode(sort_by)
    # setup cl for user preferences
    if user_pref:
        setup_user_pref(cl, user_pref)
    # search for the given query
    cl.Query(query)
    return cl.query, cl.hits, cl.facets


def compute_facet(query, fname, visu_type=''):
    # get the sphinx client
    cl = get_sphinx_client(query)
    # get the facet
    facet = cl.facets.GetFacet(fname)
    facet.AttachSphinxClient(cl)
    # very hackish here (this is what should have been done by Query
    # but since RunQueries is called instead we need to do it manually)
    if isinstance(cl, simsearch.SimClient):
        cl.query = cl.query_parser.Parse(query)
        item_ids = cl.query.GetItemIds()
        log_scores = dict(cl.DoSimQuery(item_ids))
        cl._SetupSphinxClient(item_ids, log_scores)
    # parse the query using query parser
    query = cl.query_parser.Parse(query)
    # always enable the facet
    facet.SetEnable()
    # override setup by visualisation
    if visu_type:
        config.visu[visu_type].setup(facet)
    # compute and return the results
    query.ALLOW_EMPTY = True
    facet.Compute(query)

    return facet


def get_facets_from_cache(query, user_pref={}):
    # get all the facets
    cl = get_sphinx_client(query)
    # parse the query using query parser
    query = cl.query_parser.Parse(query)
    # override user preferences
    if user_pref:
        setup_user_pref(cl, user_pref)
    # return the facets from the cache if found
    #cl.SetConnectTimeout(100.0)
    query.ALLOW_EMPTY = True
    if cl.facets:
        cl.facets.Compute(query)
    return cl.facets


def setup_user_pref(cl, user_pref):
    for facet in cl.facets:
        collapsed = user_pref['collapsed'].get(facet.name)
        visu_type = user_pref['selected_visu'].get(facet.name)
        facet.SetEnable(not collapsed)
        if visu_type:
            config.visu[visu_type].setup(facet)


def is_sim_query(query, is_active=False):
    if not config.sim_cl:
        return False
    if isinstance(query, simsearch.QuerySimilar):
        return query.GetItemIds() if is_active else True
    else:
        s = '' if is_active else '-'
        return re.search('@[+%s]?similar\s' % s, getattr(query, 'user', query))


def to_sim_query(query):
    if not isinstance(query, simsearch.QuerySimilar):
        return config.sim_cl.query_parser.Parse(getattr(query, 'user', query))
    else:
        return query

from cloudmining.app.models import items
import cite_query


def search(query, offset=0, limit=10, sort_by='', user_pref={}):
    # get the sphinx client
    cl = items.get_sphinx_client(query)
    # to restrict to cited pmids
    if cite_query.is_cite_query(query):
        query = cite_query.handle_cite_query(cl, query)
    # set page number and limit
    # stop having processed 2*500 results (see optimization)
    cl.SetLimits(offset, limit, cutoff=500)
    # set the sort by order
    if sort_by:
        cl.SetSortMode(sort_by)
    # setup cl for user preferences
    if user_pref:
        items.setup_user_pref(cl, user_pref)
    # search for the given query
    cl.Query(query)
    return cl.query, cl.hits, cl.facets


items.search = search

import web
import fsphinx

from cloudmining.app.models import items
from cloudmining.app.models import user_pref
from cloudmining.lib import paging
from cloudmining.app.helpers import templating

config = web.config
view = web.config.view


class front_page:
    def GET(self):
        pref = user_pref.reset()
        facets = items.get_facets_from_cache('', pref)
        return view.layout(view.front_page(facets, pref))


class search:
    def GET(self):
        i = web.input(previous_query='', query_inactive='', params='',
            search_mode='', q='', query='')
        # maintain compatibility with old urls
        query = i.q or i.query
        # searching in all results in current
        if i.search_mode == 'in_results':
            query = i.previous_query + ' ' + query
        else:
            query = i.query_inactive + ' ' + query
        # redirect to a pretty url
        url = fsphinx.QueryToPrettyUrl(query)
        raise web.redirect('/search/' + url + '?' + i.params)


class search_url:
    def GET(self, path):
        # get variables including the user preferences
        i = web.input(s=0, so='', ot='')
        start = int(i.s)
        pref = user_pref.get()
        # transform pretty url path into a query
        query = fsphinx.PrettyUrlToQuery(path, order=i.ot)
        # call model to search the items
        query, hits, facets = items.search(query, start, config.results_per_page, i.so, pref)
        # handle empty result set
        if not hits.total_found:
            facets = items.get_facets_from_cache('', pref)
        # create a pager to go through the results
        pager = paging.get_paging(start, hits['total_found'],
            results_per_page=config.results_per_page, window_size=config.paging_window_size)
        # call the proper view to display the results
        return view.layout(view.search(query, hits, facets, pager, pref))


class load_facet:
    def GET(self, fname, visu_type):
        i = web.input(q='')
        facet = items.compute_facet(i.q, fname, visu_type)
        return config.visu[visu_type].render(facet, animate=True)

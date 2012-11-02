import web

from cloudmining.lib.templating import public
from cloudmining.lib import utils
from cloudmining.app.models.items import is_sim_query, to_sim_query


def sort_facets(facets, ui_facets=[]):
    facet_names = (f['name'] for f in ui_facets)
    return list(utils.filter_by_keys(facets,
        key=lambda (x): x.name, keys=facet_names))


public(dict(
    is_sim_query = is_sim_query,
    to_sim_query = to_sim_query,
    normalize = utils.normalize,
    config = web.config,
    view = web.config.view,
    sort_facets = sort_facets
))

import web
import re
import fsphinx

db = web.config.cl.db_fetch._db


class QueryTermCite(fsphinx.QueryTerm):
    p_id = re.compile('^\s*(\d+)', re.I|re.U)

    def __init__(self, status, term):
        fsphinx.QueryTerm.__init__(self, status, 'cite', term)

    @property
    def sphinx(self):
        return ''


def get_cited_pmids(pmid):
    rows = db.select('pmc_citations',
        vars  = dict(pmid=pmid),
        what  = 'pmid',
        where = 'cited_pmid in $pmid')
    return [r.pmid for r in rows if r.pmid]


def is_cite_query(query):
    return re.search('\(@[+-]?cite\s+\d+\)', query)


def handle_cite_query(cl, query):
    if not isinstance(query, fsphinx.MultiFieldQuery):
        query = cl.query_parser.Parse(query)
        
    item_ids = []
    for i, qt in enumerate(query):
        if qt.user_field == 'cite':
            query._qts[i] = QueryTermCite(qt.status, qt.term)
            item_ids.append(int(qt.term))

    if item_ids:
        cl.SetFilter('pmid_attr', get_cited_pmids(item_ids))
        fsphinx.MultiFieldQuery.ALLOW_EMPTY = True
    return query

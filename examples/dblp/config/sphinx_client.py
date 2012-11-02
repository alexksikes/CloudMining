import sphinxapi
import web
import fsphinx

from fsphinx import FSphinxClient, Facet, DBFetch, MultiFieldQuery, QueryParser, hits

db = web.database(dbn='mysql', db='dblp_sample', user='fsphinx', passwd='fsphinx')

# turn db printing off
db.printing = False

redis_cache = fsphinx.RedisCache(db=0)

# make sure multi value fields are not chopped off
db.query('set group_concat_max_len = 50000')

## create sphinx client
cl = FSphinxClient()

# connect to searchd
cl.SetServer('localhost', 10000)

# we don't accept queries which take longer than 10 sec.
cl.SetConnectTimeout(10.0)

# matching mode (faceted client should be SPH_MATCH_EXTENDED2)
cl.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED2)

# specify different sorting options
cl.SetSortModeOptions({
    'cit' : (sphinxapi.SPH_SORT_EXTENDED, 'citation_counts_attr desc, @relevance desc, year_attr desc'),
    'rel' : (sphinxapi.SPH_SORT_EXTENDED, '@relevance desc'),
    'dat' : (sphinxapi.SPH_SORT_EXTENDED, 'year_attr desc')
})

# default sorting mode
cl.SetSortMode('cit')

# set the default index to search
cl.SetDefaultIndex('publications')

# some fields could matter more than others
# cl.SetFieldWeights({'field' : 30})

# sql query to fetch the hits
db_fetch = DBFetch(db, sql = '''
select
    p.id, title, source, source_id, year, url, mdate, ee,
    volume, number, pages,
    group_concat(distinct author order by author_num separator '@#@') as authors,
    c.counts as citation_counts, cid
from pub as p
left join citeseerx_citations as c on p.id = c.id,
author_ref as a
where
    p.id = a.id and p.id in ($id)
group by a.id
order by field(p.id, $id)''', post_processors = [
    hits.SplitOnSep('authors', sep='@#@'),
]
)
cl.AttachDBFetch(db_fetch)

# provide search cache
#cl.AttachCache(redis_cache)

# setup the different facets
cl.AttachFacets(
    Facet('author', sql_col='author', sql_table='author_terms', sph_field='authors'),
    Facet('keyword', sql_col='tag', sql_table='title_terms', attr='title_attr', sph_field='title'),
    Facet('venue', sql_col='source_id', sql_table='venue_terms', sph_field='source_id'),
    Facet('year', sql_table=None)
)

# we want to group by counts
group_sort = '@count desc'

# setup sorting and ordering of each facet
for f in cl.facets:
    f.SetMaxNumValues(15)
    # group by a custom function
    f.SetGroupSort(group_sort)
    # order the term alphabetically within each facet
    f.SetOrderBy('@term', order='asc')

# the query should always be parsed beforehand
query_parser = QueryParser(MultiFieldQuery, user_sph_map={
    'author' : 'authors',
    'keyword' : 'title',
    'venue' : 'source_id',
    'year' : 'year',
})
cl.AttachQueryParser(query_parser)

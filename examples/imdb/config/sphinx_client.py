import web
import sphinxapi

import fsphinx
from fsphinx import FSphinxClient, Facet, DBFetch, MultiFieldQuery, QueryParser, hits

# database parameters
db = web.database(dbn='mysql', db='fsphinx', user='fsphinx', passwd='fsphinx')

# redis cache pparameters
redis_cache = fsphinx.RedisCache(db=1)

# show output of mysql statements
db.printing = False

# make sure multi value fields are not chopped off
db.query('set group_concat_max_len = 50000')

# create sphinx client
cl = FSphinxClient()

# connect to searchd
cl.SetServer('localhost', 10001)

# we don't accept queries which take longer than 2 sec.
#cl.SetConnectTimeout(2.0)

# matching mode (faceted client should be SPH_MATCH_EXTENDED2)
cl.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED2)

# specify different sorting options
cl.SetSortModeOptions({
    'pop' : (sphinxapi.SPH_SORT_EXPR, '@weight * user_rating_attr * nb_votes_attr * year_attr / 100000'),
    'dat' : (sphinxapi.SPH_SORT_EXTENDED, 'year_attr desc'),
    'rat' : (sphinxapi.SPH_SORT_EXTENDED, 'user_rating_attr desc'),
    'vot' : (sphinxapi.SPH_SORT_EXTENDED, 'nb_votes_attr desc')
})

# default sorting mode
cl.SetSortMode('pop')

# sorting and possible custom sorting function
cl.SetSortMode(sphinxapi.SPH_SORT_EXPR, '@weight * user_rating_attr * nb_votes_attr * year_attr / 100000')

# set the default index to search
cl.SetDefaultIndex('items')

# some fields could matter more than others
cl.SetFieldWeights({'title' : 30})

# sql query to fetch the hits
db_fetch = DBFetch(db, sql = '''
select
    imdb_id as id,
    filename, title, year, user_rating, nb_votes, type_tv_serie, type_other,
    release_date, release_date_raw, plot, awards, runtime,
    color, aspect_ratio, certification,
    cover_url, gallery_url, trailer_url, release_date_raw,
    (select group_concat(distinct director_name separator '@#@') from directors as d where d.imdb_id = t.imdb_id) as director,
    (select group_concat(distinct actor_name separator '@#@') from casts as c where c.imdb_id = t.imdb_id) as actor,
    (select group_concat(distinct genre separator '@#@') from genres as g where g.imdb_id = t.imdb_id) as genre,
    (select group_concat(distinct plot_keyword separator '@#@') from plot_keywords as p where p.imdb_id = t.imdb_id) as keyword
from titles as t
where imdb_id in ($id)
order by field(imdb_id, $id)''', post_processors = [
    hits.SplitOnSep('director', 'actor', 'genre', 'keyword', sep='@#@')
]
)
cl.AttachDBFetch(db_fetch)

# give it a cache for the search and the facets
cl.AttachCache(redis_cache)

# setup the different facets
cl.AttachFacets(
    Facet('year', sql_table=None),
    Facet('genre'),
    Facet('keyword', attr='plot_keyword_attr', sql_col='plot_keyword', sql_table='plot_keyword_terms'),
    Facet('director'),
    Facet('actor'),
)

# for all facets compute count, groupby and this score
group_func = '''
sum(
    if (runtime_attr > 45,
        if (nb_votes_attr > 1000,
            if (nb_votes_attr < 10000, nb_votes_attr * user_rating_attr, 10000 * user_rating_attr),
        1000 * user_rating_attr),
    300 * user_rating_attr)
)'''

# setup sorting and ordering of each facet
for f in cl.facets:
    f.SetGroupFunc(group_func)
    # order the term alphabetically within each facet
    f.SetOrderBy('@term', order='asc')

# the query should always be parsed beforehand
query_parser = QueryParser(MultiFieldQuery, user_sph_map={
    'genre' : 'genres',
    'keyword' : 'plot_keywords',
    'director' : 'directors',
    'actor' : 'actors'
})
cl.AttachQueryParser(query_parser)

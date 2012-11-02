import sphinxapi
import web
import fsphinx

from fsphinx import FSphinxClient, Facet, DBFetch, MultiFieldQuery, QueryParser, hits

# connect to database
db = web.database(dbn='mysql', db='medline_sample', user='fsphinx', passwd='fsphinx')

# turn db printing off
db.printing = False

# make sure we don't chop off
db.query('set group_concat_max_len = 5000')

# create sphinx client
cl = FSphinxClient()

# connect to searchd
cl.SetServer('localhost', 10003)

# we don't accept queries which take longer than 2 sec.
cl.SetConnectTimeout(20.0)

# provide search cache
cl.AttachCache(fsphinx.RedisCache(db=2))

# matching mode (faceted client should be SPH_MATCH_EXTENDED2)
cl.SetMatchMode(sphinxapi.SPH_MATCH_EXTENDED2)

# sorting and possible custom sorting function
# use natural order of document ids (see optimization)
cl.SetRankingMode(sphinxapi.SPH_RANK_NONE)
cl.SetSortMode(sphinxapi.SPH_SORT_EXTENDED, '@rank asc')

# sql query to fetch the hits
db_fetch = DBFetch(db, 
    getter = lambda x: x['attrs']['pmid_attr'], 
    sql = '''select
        pmid,
        title,
        book_title,
        year,
        journal_title_abbreviation,
        volume,
        issue,
        pagination,
        source,
        pmc_id,
        (select group_concat(distinct mesh_term separator "@#@") from mesh as m where m.pmid = c.pmid) as mesh,
        (select group_concat(distinct author separator "@#@") from authors as a where a.pmid = c.pmid) as authors,
        (select count from pmc_num_citations as p where p.pmid = c.pmid) as citation_count
        from citations as c
        where pmid in ($id)
        order by field(pmid, $id)''', 
    post_processors = [
        hits.SplitOnSep('mesh', 'authors', sep='@#@'),
    ]
)
cl.AttachDBFetch(db_fetch)

# setup the different facets
cl.AttachFacets(
    Facet('author', sph_field='authors'),
    Facet('journal', sph_field='journal_title_abbreviation'),
    Facet('mesh', attr='mesh_attr', sql_col='mesh_term', sql_table='mesh_terms_terms'),
    Facet('year', sql_table=None),
)

# setup sorting and ordering of each facet
for f in cl.facets:
    # group by a custom function
    f.SetGroupFunc('sum(citation_count_attr)')
#    f.SetGroupSort('@count desc')
    # order the term alphabetically within each facet
    f.SetOrderBy('@term', order='asc')
    # fixes Sphinx bug: SetSelect with distributed indexes
    f._set_select = f._set_select + ', %s, %s, pmid_attr, citation_count_attr' % (f._attr, 'year_attr')
    # stop after having processed 500 results (see optimization)
    f.SetCutOff(500)

# the query should always be parsed beforehand
query_parser = QueryParser(MultiFieldQuery, user_sph_map={
    'author' : 'authors',
    'journal' : 'journal_title_abbreviation',
    'mesh' : 'mesh',
    'year' : 'year',
})
cl.AttachQueryParser(query_parser)

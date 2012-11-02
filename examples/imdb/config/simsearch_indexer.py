# database parameters
db_params = dict(user='fsphinx', passwd='fsphinx', db='fsphinx')

# list of SQL queries to fetch the features from
sql_features = [
    'select imdb_id as item_id, plot_keyword as feature from plot_keywords',
#    'select g.imdb_id as item_id, genre as feature from titles as t, genres as g where t.imdb_id = g.imdb_id',
#    'select d.imdb_id as item_id, director_name as feature from titles as t, directors as d where t.imdb_id = d.imdb_id',
]

# path to read or save the index
index_path = 'data/sim-index/'

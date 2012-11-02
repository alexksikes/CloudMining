# database parameters
db_params = dict(user='fsphinx', passwd='fsphinx', db='dblp_sample')

# list of SQL queries to fetch the features from
sql_features = [
    # title keywords
    'select id as item_id, tag as feature from pub_title_terms',
    # authors
    'select id as item_id, author as feature from author_ref',
    # venues
    'select id as item_id, source_id as feature from pub',
    # years
    'select id as item_id, year as feature from pub',
]

index_path = 'data/sim-index/'

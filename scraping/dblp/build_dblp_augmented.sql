# for sphinx, assign a keyword title tag to each publication
drop table if exists pub_title_tags;
create table pub_title_tags (
    id                      int(32) unsigned not null,
    tag                     varchar(70) not null,
    tag_id                  int(32) unsigned not null,
    index(tag_id),
    primary key (id, tag_id)
) charset utf8;
load data infile '/projects/data/cloudmining/dblp/keywords/tag_pub_title.txt' into table pub_title_tags (id, @dummy, tag, tag_id);

# for sphinx, lookup table from title attr to title tags
drop table if exists title_tags;
create table title_tags (
    id                      int(32) unsigned primary key,
    tag                     varchar(70) not null
) charset utf8;
load data infile '/projects/data/cloudmining/dblp/keywords/tag_ids.txt' into table title_tags (id, tag);

# number citation for a given article id using citeseerx
drop table if exists citeseerx_citations;
create table citeseerx_citations (
    id                      int(32) unsigned primary key,
    counts                  int(11),
    cid                     int(11)
) charset utf8;
load data infile '/projects/data/cloudmining/dblp/citeseerx/citation_counts.txt' into table citeseerx_citations (id, @dummy, counts, cid);

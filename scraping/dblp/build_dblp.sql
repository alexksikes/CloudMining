# We use the DB from FacetedDBLP (http://dblp.l3s.de/dblp++.php).
alter table dblp_pub_new rename pub;
alter table dblp_author_ref_new rename author_ref;
alter table author_ref add index(author);

# for sphinx, lookup table from crc32(source_id) to venue names
create table venue_tags (
    id                      int(32) unsigned primary key,
    source_id               varchar(50) not null,
    source                  varchar(150),
    index(source_id)
) charset utf8;

# populate the venue tags
insert venue_tags 
    select crc32(source_id), source_id, source 
    from pub 
    where source_id is not NULL 
    group by crc32(source_id) 
    order by source_id;

# for sphinx, lookup table from author attr to author names
create table author_tags (
    id                      int(32) unsigned primary key,
    author                  varchar(70) not null,
    index(author)
) charset utf8;

# populate the author tags (we can't use crc32 due to collisions)
set @i := 0; 
insert author_tags 
    select @i := @i + 1, author 
    from author_ref
    where author is not NULL 
    group by author 
    order by author;

# cache used for costly queries (especially to compute facets)
create table cache (
    query                   varchar(70) primary key,
    facets                  text
) charset utf8;

# for sphinx, assign a keyword title tag to each publication
create table pub_title_tags (
    id                      int(32) unsigned not null,
    tag                     varchar(70) not null,
    tag_id                  int(32) unsigned not null,
    index(tag_id),
    primary key (id, tag_id)
) charset utf8;
load data infile '/projects/scripts/dblp/tag_pub_title.txt' into table pub_title_tags (id, @dummy, tag, tag_id);

# for sphinx, lookup table from title attr to title tags
create table title_tags (
    id                      int(32) unsigned primary key,
    tag                     varchar(70) not null
) charset utf8;
load data infile '/projects/scripts/dblp/tag_ids.txt' into table title_tags (id, tag);

# number citation for a given article id using citeseerx
create table citeseerx_citations (
    id                      int(32) unsigned primary key,
    counts                  int(11),
    cid                     int(11)
) charset utf8;
load data infile '/projects/scripts/dblp/script/citeseerx/citation_counts.txt' into table citeseerx_citations (id, @dummy, counts, @dummy);

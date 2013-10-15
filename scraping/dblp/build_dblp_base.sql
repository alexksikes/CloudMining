# We use the DB from FacetedDBLP (http://dblp.l3s.de/dblp++.php).
# removing unecessary tables from the dump
drop table if exists dblp_aliases_new;
drop table if exists dblp_authorid_ref_new;
drop table if exists dblp_main_aliases_new;
drop table if exists dblp_ref_new;

# removing old tables
drop table if exists pub;
drop table if exists author_ref;

# replacing with new tables
alter table dblp_pub_new rename pub;
alter table dblp_author_ref_new rename author_ref;
alter table author_ref add index(author);

# for sphinx, lookup table from crc32(source_id) to venue names
drop table if exists venue_tags;
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
drop table if exists author_tags;
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

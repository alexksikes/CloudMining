# this is for me, do not use!
# sql file that was used to build the test database from the real DBLP database

# let's get the most cited articles on dblp
create table dblp_sample.pub like dblp.pub;
insert dblp_sample.pub 
    select p.* 
        from dblp.pub as p, dblp.citeseerx_citations as c 
    where p.id = c.id 
    order by c.counts desc limit 10000;

# venues
create table dblp_sample.venue_terms like dblp.venue_tags;
insert dblp_sample.venue_terms
    select crc32(source_id), source_id, source 
        from dblp_sample.pub 
    where source_id is not NULL 
    group by crc32(source_id) 
    order by source_id;
    
# authors
create table dblp_sample.author_ref like dblp.author_ref;
insert dblp_sample.author_ref 
    select t1.*
        from dblp.author_ref as t1
    inner join dblp_sample.pub as t2 
        where t1.id = t2.id;

create table dblp_sample.author_terms like dblp.author_tags;
set @i := 0; 
insert dblp_sample.author_terms
    select @i := @i + 1, author 
        from dblp_sample.author_ref
    where author is not NULL 
    group by author 
    order by author;

# keywords
create table dblp_sample.pub_title_terms like dblp.pub_title_tags;
insert dblp_sample.pub_title_terms 
    select t1.*
        from dblp.pub_title_tags as t1
    inner join dblp_sample.pub as t2 
        where t1.id = t2.id;

create table dblp_sample.title_terms like dblp.title_tags;
insert dblp_sample.title_terms 
    select t1.*
        from dblp.title_tags as t1
    inner join dblp_sample.pub_title_terms as t2 
        where t1.id = t2.tag_id
    group by t2.tag_id;

# number citation for a given article id using citeseerx
create table dblp_sample.citeseerx_citations like dblp.citeseerx_citations;
insert dblp_sample.citeseerx_citations 
    select t1.*
        from dblp.citeseerx_citations as t1
    inner join dblp_sample.pub as t2 
        where t1.id = t2.id;

# create the dblp_sample user for testing ...
create user 'fsphinx'@'localhost' identified by 'fsphinx';
grant select on dblp_sample.* to 'fsphinx'@'localhost';

# dump the schema only and full data and get into mysql
# >> mysqldump --no-data -p dblp_sample > sql/dblp_top10000.schema.sql
# >> mysqldump -p dblp_sample > sql/dblp_top10000.data.sql
# >> mysql -u fsphinx -D dblp_sample -p

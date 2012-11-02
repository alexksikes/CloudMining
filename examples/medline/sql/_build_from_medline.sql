# this is for me, do not use!
# sql file that was used to build the test database from the real MEDLINE database

# let's get the most popular movies on imdb
create table medline_sample.citations like medline.citations;
insert medline_sample.citations 
    select t1.*
        from medline.citations as t1, medline.pmc_num_citations as t2 
    where t1.pmid = t2.pmid
    order by t2.count desc limit 10000;

# journals
create table medline_sample.journal_terms like medline.journal_terms;
set @i := 0; 
insert medline_sample.journal_terms
    select @i := @i + 1, journal_title_abbreviation 
        from medline_sample.citations
    group by journal_title_abbreviation  
    order by journal_title_abbreviation;

# authors
create table medline_sample.authors like medline.authors;
insert medline_sample.authors 
    select t1.*
        from medline.authors as t1
    inner join medline_sample.citations as t2 
        where t1.pmid = t2.pmid;
    
create table medline_sample.author_full_names like medline.author_full_names;
insert medline_sample.author_full_names 
    select t1.*
        from medline.author_full_names as t1
    inner join medline_sample.citations as t2 
        where t1.pmid = t2.pmid;

create table medline_sample.author_terms like medline.author_terms;
set @i := 0;
insert medline_sample.author_terms 
    select @i := @i + 1, author
        from medline_sample.authors
    group by author
    order by author;
    
# mesh terms
create table medline_sample.mesh like medline.mesh;
insert medline_sample.mesh 
    select t1.*
        from medline.mesh as t1
    inner join medline_sample.citations as t2 
        where t1.pmid = t2.pmid;
    
create table medline_sample.mesh_terms like medline.mesh_terms;
insert medline_sample.mesh_terms 
    select t1.*
        from medline.mesh_terms as t1
    inner join medline_sample.citations as t2 
        where t1.pmid = t2.pmid;

create table medline_sample.mesh_terms_terms like medline.mesh_terms_terms;
set @i := 0;
insert medline_sample.mesh_terms_terms 
    select @i := @i + 1, mesh_term
        from medline_sample.mesh_terms
    group by mesh_term
    order by mesh_term;
    
# pmc citations
create table medline_sample.pmc_citations like medline.pmc_citations;
insert medline_sample.pmc_citations 
    select t1.*
        from medline.pmc_citations as t1
    inner join medline_sample.citations as t2 
        where t1.pmid = t2.pmid;

create table medline_sample.pmc_num_citations like medline.pmc_num_citations;
insert medline_sample.pmc_num_citations 
    select t1.*
        from medline.pmc_num_citations as t1
    inner join medline_sample.citations as t2 
        where t1.pmid = t2.pmid;

# publication types
create table medline_sample.publication_types like medline.publication_types;
insert medline_sample.publication_types 
    select t1.*
        from medline.publication_types as t1
    inner join medline_sample.citations as t2 
        where t1.pmid = t2.pmid;

# create the fsphinx user for testing ...
create user 'fsphinx'@'localhost' identified by 'fsphinx';
grant select on medline_sample.* to 'fsphinx'@'localhost';
    
# for optimization .. (used for the full instance)
drop table if exists docids;
create table docids (
    pmid                    int(32) unsigned primary key,
    docid                   int(32) unsigned
) charset utf8;

set @id := 0;
insert docids
    select pmid, @id := @id + 1 as docid from (
        select c.pmid 
        from citations as c
        left join pmc_num_citations as p 
        on c.pmid = p.pmid 
        order by p.count desc, c.pmid desc) as t;
alter table docids add index(docid);

# dump the schema only and full data and get into mysql
# >> mysqldump --no-data -p medline_sample > sql/medline_top10000.schema.sql
# >> mysqldump -p medline_sample > sql/medline_top10000.data.sql
# >> mysql -u fsphinx -D medline_sample -p
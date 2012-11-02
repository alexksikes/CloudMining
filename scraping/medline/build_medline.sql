# Make sure the database is UTF-8 (needed for load data infile)
# create database medline default charset utf8; use medline;

# May be needed for very large dataset in order to prevent "repair by key cache" (very slow)
# and to get "repair by sorting" (much faster).
# set session myisam_max_sort_file_size = 100*1024*1024*1024;
# set session myisam_sort_buffer_size = 1500*1024*1024;

use medline;
# We start with a scape of MEDLINE  (see scripts/scraping).
# python mass_scrapping/populate.py -d conf/citations.conf /projects/scripts/medline.scraping/sample/tables/citations.tbl citations
# python mass_scrapping/populate.py -d conf/authors.conf /projects/scripts/medline.scraping/sample/tables/authors.tbl authors
# python mass_scrapping/populate.py -d conf/author_full_names.conf /projects/scripts/medline.scraping/sample/tables/author_full_names.tbl author_full_names
# python mass_scrapping/populate.py -d conf/mesh.conf /projects/scripts/medline.scraping/sample/tables/mesh.tbl mesh
# python mass_scrapping/populate.py -d conf/publication_types.conf /projects/scripts/medline.scraping/sample/tables/publication_types.tbl publication_types

# After having run get_mesh_terms.py on mesh_terms.tbl
# python mass_scrapping/populate.py -d conf/mesh.conf /projects/scripts/medline.scraping/sample/tables/mesh_terms.tbl mesh_terms

# Remove Et Al. from the authors
alter table authors add index(author);
delete from authors where author = 'Et Al.';
delete from author_full_names where author_full_name = 'Et Al.';

# For the journal facet
drop table if exists journal_terms;
create table journal_terms (
    id                      int(32) unsigned primary key,
    journal                 varchar(150)
) charset utf8;

alter table citations add index(journal_title_abbreviation);
set @i := 0; 
insert journal_terms
    select @i := @i + 1, journal_title_abbreviation 
    from citations
    group by journal_title_abbreviation  
    order by journal_title_abbreviation;

# For the author facet
drop table if exists author_terms;
create table author_terms (
    id                      int(32) unsigned primary key,
    author                  varchar(100)
) charset utf8;

# alter table authors add index(author);
set @i := 0;
insert author_terms 
    select @i := @i + 1, author
    from authors
    group by author
    order by author;
    
# For the mesh terms facet
drop table if exists mesh_terms_terms;
create table mesh_terms_terms (
    id                      int(32) unsigned primary key,
    mesh_term               varchar(100)
) charset utf8;

alter table mesh_terms add index(mesh_term);
set @i := 0;
insert mesh_terms_terms 
    select @i := @i + 1, mesh_term
    from mesh_terms
    group by mesh_term
    order by mesh_term;

# Cache used for costly queries (especially to compute facets)
drop table if exists cache; 
create table cache (
    _key                    varchar(32) primary key,
    comment                 text,
    value                   blob,
    sticky                  boolean,
    datetime                timestamp default current_timestamp
) charset utf8 engine MyISAM;
    
# Help Sphinx query
alter table authors add index(pmid);
alter table author_full_names add index(pmid);
alter table mesh add index(pmid);
alter table mesh_terms add index(pmid);

# Help Sphinx indexing
alter table journal_terms add index(journal);
alter table author_terms add index(author);
alter table mesh_terms_terms add index(mesh_term);

# For citation information
# python mass_scrapping/populate.py -d conf.pmc/pmc_citations.conf /projects/scripts/medline.scraping/sample/tables/pmc_citations.tbl pmc_citations
alter table pmc_citations add index(pmid);
alter table pmc_citations add index(cited_pmid);
create table pmc_num_citations (
    pmid                    int(12) unsigned primary key,
    count                   int(12)
) charset utf8;
insert pmc_num_citations 
    select cited_pmid, count(pmid) 
    from pmc_citations 
    group by cited_pmid;

# for Sphinx indexing in order to use natural order (and not have to sort)
drop table if exists docids;
create table docids (
    pmid                    int(32) unsigned primary key,
    docid                   int(32) unsigned
) charset utf8;

set @id := 0;
insert docids
    select c.pmid, @id := @id + 1 as docid 
    from citations as c
    left join pmc_num_citations as p 
    on c.pmid = p.pmid 
    order by p.count desc, c.pmid desc;

alter table docids add index(docid);

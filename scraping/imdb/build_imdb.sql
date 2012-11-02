# Make sure the database is UTF-8 (needed for load data infile)
create database movies default charset utf8; use movies;

# We start with a scape of IMDB  (see scripts/scraping).
# python populate.py -d conf/titles.conf /projects/data/imdb/tables/titles.tbl titles
# python populate.py -d conf/directors.conf /projects/data/imdb/tables/directors.tbl directors
# python populate.py -d conf/writers.conf /projects/data/imdb/tables/writers.tbl writers
# python populate.py -d conf/casts.conf /projects/data/imdb/tables/casts.tbl casts
# python populate.py -d conf/genres.conf /projects/data/imdb/tables/genres.tbl genres
# python populate.py -d conf/plot_keywords.conf /projects/data/imdb/tables/plot_keywords.tbl plot_keywords

# python populate.py -d conf/recommendations.conf /projects/data/imdb/tables/recommendations.tbl recommendations
# python populate.py -d conf/company.conf /projects/data/imdb/tables/company.tbl company
# python populate.py -d conf/country.conf /projects/data/imdb/tables/country.tbl country
# python populate.py -d conf/language.conf /projects/data/imdb/tables/language.tbl language

# First some cleaning on the titles table
delete from titles where imdb_id = 0 or type_episode = 1 or title is NULL;
update titles set release_date = NULL where release_date = '0000-00-00';
delete from titles where type_other = 'VG' or type_other = 'TV';

# Trim out the porn
create temporary table keep select t.* from titles as t, genres as g where t.imdb_id = g.imdb_id 
and g.genre= 'Adult' and (cover_url is not NULL or (user_rating > 0.7 and nb_votes > 5)) group by t.imdb_id;
delete titles from titles inner join genres where titles.imdb_id = genres.imdb_id and genres.genre = 'Adult';
insert titles select * from keep;

# Remove

# Make the director tags
create table director_tags (
    id                      int(32) unsigned primary key,
    director                varchar(250) not null
) charset utf8;

# Populate the director tags
alter table directors add index(imdb_director_id);
insert director_tags 
    select imdb_director_id, director_name 
    from directors
    group by imdb_director_id; 

# Make the writer tags
create table writer_tags (
    id                      int(32) unsigned primary key,
    director                varchar(250) not null
) charset utf8;

# Populate writer tags
alter table writers add index(imdb_writer_id);
insert writer_tags 
    select imdb_writer_id, writer_name 
    from writers
    group by imdb_writer_id;

# Create actor tags
create table actor_tags (
    id                      int(32) unsigned primary key,
    actor                   varchar(250) not null
) charset utf8;    

# Populate genre tags    
alter table casts add index(imdb_actor_id)
insert actor_tags 
    select imdb_actor_id, actor_name 
    from casts
    group by imdb_actor_id;
    
# Make the genre tags
create table genre_tags (
    id                      int(32) unsigned primary key,
    genre                   varchar(70) not null
) charset utf8;

# Populate the genre tags
alter table genres add index(genre)
set @i := 0; 
insert genre_tags 
    select @i := @i + 1, genre 
    from genres
    group by genre 
    order by genre;

# Create plot keyword tags
create table plot_keyword_tags (
    id                      int(32) unsigned primary key,
    plot_keyword            varchar(70) not null
) charset utf8;

# Populate plot keyword tags
alter table plot_keywords add index(plot_keyword);
set @i := 0; 
insert plot_keyword_tags 
    select @i := @i + 1, plot_keyword 
    from plot_keywords
    group by plot_keyword 
    order by plot_keyword;

# Make the recommendation tags
create table recommendation_tags (
    id                      int(32) unsigned primary key,
    title                   varchar(250) not null
) charset utf8;

# Populate recommendation tags
alter table recommendations add index(imdb_rec_id);
insert recommendation_tags 
    select imdb_rec_id, title_name 
    from recommendations
    group by imdb_rec_id;

# Have the ratings in the same table as recommendations
# This is actually not used.
create temporary table keep select r.filename, r.imdb_id, imdb_rec_id, title_name, user_rating 
from recommendations as r, titles as t where r.imdb_rec_id = t.imdb_id;
delete from recommendations;
insert recommendations select * from keep;
drop table keep;
    
# Make the company tags
create table company_tags (
    id                      int(32) unsigned primary key,
    title                   varchar(250) not null
) charset utf8;

# Populate company tags
alter table company add index(company_id);
insert company_tags 
    select company_id, company_name 
    from company
    group by company_id;

# Make the country tags
create table country_tags (
    id                      int(32) unsigned primary key,
    country                 varchar(250) not null
) charset utf8;

# Populate plot country tags
alter table country add index(country);
set @i := 0; 
insert country_tags 
    select @i := @i + 1, country
    from country
    group by country 
    order by country;

# Make the language tags
create table language_tags (
    id                      int(32) unsigned primary key,
    language                varchar(250) not null
) charset utf8;

# Populate language tags
alter table language add index(language);
set @i := 0; 
insert language_tags 
    select @i := @i + 1, language 
    from language
    group by language 
    order by language;

# Make the certification tags
create table certification_tags (
    id                      int(32) unsigned primary key,
    certification           varchar(15) not null
) charset utf8;

# Populate certification tags
alter table titles add index(certification);
insert certification_tags 
    select crc32(certification), certification
    from titles
    group by certification 
    order by certification;
    
# Cache used for costly queries (especially to compute facets)
create table cache (
    query                   varchar(70) primary key,
    facets                  text
) charset utf8;

# Help sphinx query
alter table directors add index(imdb_id);
alter table casts add index(imdb_id);
alter table writers add index(imdb_id);
alter table genres add index(imdb_id);
alter table plot_keywords add index(imdb_id);
alter table recommendations add index(imdb_id);
alter table company add index(imdb_id);
alter table country add index(imdb_id);
alter table language add index(imdb_id);

alter table genre_tags add index(genre);
alter table plot_keyword_tags add index(plot_keyword);

# Later we added all the keywords found on IMDb
# python populate.py -d conf/more_plot_keywords.conf /projects/data/imdb/tables/more_plot_keywords.tbl more_plot_keywords
alter table more_plot_keywords add index(imdb_id); 
alter table more_plot_keywords add index(plot_keyword);

# Create a table with all the keywords (we only downloaded the all the 
# keywords if we had mre than 4 keywords already)
create temporary table test select imdb_id from plot_keywords group by imdb_id having count(imdb_id) <= 4;
alter table test add index(imdb_id); 

create table all_plot_keywords
    select p.imdb_id, plot_keyword from plot_keywords as p, test as t where p.imdb_id = t.imdb_id;

insert all_plot_keywords
    select * from more_plot_keywords;

alter table all_plot_keywords add index(imdb_id); 
alter table all_plot_keywords add index(plot_keyword);
    
# Create all keyword tags
create table all_plot_keyword_tags (
    id                      int(32) unsigned primary key,
    plot_keyword            varchar(70) not null
) charset utf8;

# Populate all plot keyword tags
set @i := 0; 
insert all_plot_keyword_tags 
    select @i := @i + 1, plot_keyword 
    from all_plot_keywords
    group by plot_keyword 
    order by plot_keyword;
    
alter table all_plot_keyword_tags add index(plot_keyword);
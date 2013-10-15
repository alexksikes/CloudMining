Here are the steps to create/update all the data necessary for the full DBLP instance (2.4M computer science publications).

We assume the working directory is *cloudmining/scraping/dblp/* and all the data is downloaded in some other directory located at */projects/data/cloudmining/dblp/*.

1) Get the latest version of the SQL dump from [http://dblp.l3s.de/dblp++.php](http://dblp.l3s.de/dblp++.php). At the time of this writing the latest version is *dblp-2013-10-05.sql.gz*.

    cd /projects/data/cloudmining/dblp/
    wget http://dblp.l3s.de/dblp-2013-10-05.sql.gz
    gzip -d dblp-2013-10-05.sql.gz

2) If it does not already exist, create a MySQL database named *dblp*:

    mysql -pe 'create database dblp charset latin1;'

3) Load the dump into your dblp database:

    mysql -p dblp < dblp-2013-10-05.sql
    
4) Run the script *build_dblp_base.sql*:

    mysql -p dblp < build_dblp_base.sql
    
5) Follow the instructions in *./keywords/README.md* to add tags from titles.

6) Follow the instructions in *./citeseerx/README.md* to add number of citations.

7) Run the script *build_dblp_augmented.sql*:

    mysql -p dblp < build_dblp_augmented.sql

We now assume the working directory is *cloudmining/examples/dblp/*.

8) Review and set the database parameters in *./config/\**. Make sure the database is set to *dblp* (not *dblp_sample*). 

We chose to copy the directories *config/* and *data/* to *config-full/* and *data-full/* and make the changes there. We also slightly modified *application.py* to *application-full.py* to reflect the change of config files and of redis cache location (see below).

9) (Re-)Index the data with Sphinx:

    /path/to/sphinx/indexer -c ./config-full/sphinx_indexer.cfg --all

10) Let searchd serve the Sphinx index:

    /path/to/sphinx/searchd -c ./config-full/sphinx_indexer.cfg
    
11) Preload the facets with [fSphinx](https://github.com/alexksikes/fSphinx) and dump the results in *./data-full/redis-cache.dat*:

    /path/to/fsphinx/tools/preload_cache.py -fc config-full/sphinx_client.py --dump data-full/redis-cache.dat ''

12) (Re-)Index the data with [SimSearch](https://github.com/alexksikes/SimSearch):

    /path/to/simsearch/tools/index_features.py -o ./data-full/sim-index/ config-full/simsearch_indexer.py
    
13) Test everything is working with the built-in web server:
    
    python application-full.py
    
14) You're done!

    visit http://localhost:8080
We assume that the current working directory is {instance_name}/ where
{instance_name} is either dblp, imdb or medline.

1) Create a MySQL database called {instance_name}_sample with user and password
   "fsphinx". In a MySQL shell type:

    create database {instance_name}_sample character set utf8;
    
2) And a user "fsphinx" with password "fsphinx".

    create user 'fsphinx'@'localhost' identified by 'fsphinx';
    grant ALL on {instance_name}_sample.* to 'fsphinx'@'localhost';
    
3) Load the data into the database:

    mysql -u fsphinx -D {instance_name}_sample -p < ./sql/{dataset_name}.data.sql
    
4) Let Sphinx index the data:

    /path/to/sphinx/indexer -c ./config/sphinx_indexer.cfg --all
    
5) And let searchd serve the index:

    /path/to/sphinx/searchd -c ./config/sphinx_indexer.cfg

6) Let simsearch index the features (only for IMDb and DBLP):

    /path/to/simsearch/tools/index_features.py -o ./data/sim-index/ config/simsearch_indexer.py

7) Start the instance using the built webserver:
    
    python application.py
    
8) You're done!

    visit http://localhost:8080
    
Note in production (using lighttpd), your fastcgi conf would look something
like this. Do not forget the **aliases**.

    ...

    name = "{instance_name}"
    script = "/path/to/cloudmining/examples/{instance_name}/application.py"

    server.document-root = "/path/to/cloudmining/examples/{instance_name}/public/"

    alias.url = ( "/js/" => "/path/to/cloudmining/cloudmining/public/js/" )
    alias.url += ( "/img/" => "/path/to/cloudmining/cloudmining/public/img/" )
    alias.url += ( "/css/" => "/path/to/cloudmining/cloudmining/public/css/" )

    url.rewrite += (
        # Commented for development
        "^/img/(.*)$" => "/img/$1",
        "^/css/(.*)$" => "/css/$1",
        "^/js/(.*)$" => "/js/$1",
        "^/public/(.*)$" => "/$1",

        "^/(.*)$" => script + "/$1",
    )

    fastcgi.server = ( script =>
    ((
        "socket" => "/tmp/" + name + var.PID + ".socket",
        "bin-path" => script,
        "check-local" => "disable",
        "max-procs" => 1,
        "bin-environment" => (
            "REAL_SCRIPT_NAME" => ""
        ),
    ))
    )

    ...


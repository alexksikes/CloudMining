First you need to [install][1] the latest version of Sphinx if you have not
already done so. You would do something like this:

    svn checkout http://sphinxsearch.googlecode.com/svn/trunk/ sphinxsearch-read-only
    cd sphinxsearch-read-only
    ./configure --prefix=/usr/local/sphinx
    make
    sudo make install
    
Download and extract the latest Cloud Mining tarball:

    wget http://github.com/alexksikes/cloudmining/tarball/master
    tar xvzf "the tar ball"
    
Add the Cloud Mining package to your PYTHONPATH:

    export PYTHONPATH=$PYTHONPATH:/path/to/cloudmining/cloudmining

Make sure you have installed the following dependencies:

* [web.py][3] for the web interface.
* [fSphinx][4] for faceted search.
* [SimSearch][5] if you want to support similarity search.
    
You're done! 

What's next? Have a look into some [instances][6] provided to learn how to use.

[1]: http://sphinxsearch.com/docs/manual-2.0.1.html#installation
[3]: http://webpy.org/install
[4]: https://github.com/alexksikes/fSphinx/
[5]: https://github.com/alexksikes/SimSearch/
[6]: https://github.com/alexksikes/CloudMining/tree/master/examples

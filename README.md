Cloud Mining is a web interface for the [Sphinx][0] search engine. It is aimed
at encouraging nonlinear search and data exploration. It makes use of the
[fSphinx][1] module for faceted search. [SimSearch][2] is used for item based
search. The facets support different visualizations such as tag clouds,
histogram counts, a rose diagram. Other visualizations can be provided as
plugins.

Create a file called application.py with the following lines:

    from cloudmining import CloudMiningApp

    # create a new CloudMining web application
    app = CloudMiningApp()

    # create a FSphinxClient from a configuration file
    cl = FSphinxClient.FromConfig('/path/to/config/sphinx_client.py')

    # set the fsphinx client of the app
    app.set_fsphinx_client(cl)

Execute application.py and aim your browser at http://localhost:8080:

	python application.py
    
For the IMDb instance, you obtain the following interface:

![Cloud Mining Generic Interface](http://alex.ksikes.net/static/imdb.generic.png "Cloud Mining Generic Interface")

After customization you get:

![Cloud Mining Customized Interface](http://alex.ksikes.net/static/imdb.customized.png "Cloud Mining Customized Interface")

Check out some [instances][_1], [here][_2] and [there][_3]. Have a look at the
[api][3] for customization and look into some [example instances][4] provided.

Thank you to [Andy Gott][5] for the logo design, [FAMFAMFAM][6] and [Fugue][7]
for the icons. Rose diagram thanks to [RGraph][8].

[0]: http://sphinxsearch.com/
[1]: https://github.com/alexksikes/fSphinx/
[2]: https://github.com/alexksikes/SimSearch/
[3]: https://github.com/alexksikes/cloudmining/cloudmining/api.py
[4]: https://github.com/alexksikes/cloudmining/examples/
[5]: http://reallysimpleworks.com/
[6]: http://www.famfamfam.com/lab/icons/silk/
[7]: http://p.yusukekamiyamane.com/
[8]: http://www.rgraph.net/

[_1]: http://dblp.cloudmining.net
[_2]: http://imdb.cloudmining.net
[_3]: http://medline.cloudmining.net

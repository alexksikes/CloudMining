Cloud Mining automatically builds exploratory faceted search systems. It
leverages [Sphinx][0] as a full text retrieval engine and [fSphinx][1] for
faceted search. [SimSearch][2] is used for item based search. The aim is to
provide an interface which will encourage nonlinear search and data
exploration. The facets support different visualizations such as tag clouds,
histogram counts or a rose diagram and can be extended with pluggins.

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
    
On data from IMDb, you obtain the following interface:

![Cloud Mining Generic Interface](http://alex.ksikes.net/static/imdb.generic.png "Cloud Mining Generic Interface")

And after customization, you get:

![Cloud Mining Customized Interface](http://alex.ksikes.net/static/imdb.customized.png "Cloud Mining Customized Interface")

Check out some [instances][_1], [here][_2] and [there][_3]. Have a look at the
[api][3] for customization and look into some of the [example instances][4]
provided.

Thank you to [Andy Gott][5] for the logo design, [FAMFAMFAM][6] and [Fugue][7]
for the icons. Rose diagram thanks to [RGraph][8].

[0]: http://sphinxsearch.com/
[1]: https://github.com/alexksikes/fSphinx/
[2]: https://github.com/alexksikes/SimSearch/
[3]: https://github.com/alexksikes/CloudMining/blob/master/cloudmining/api.py
[4]: https://github.com/alexksikes/CloudMining/tree/master/examples
[5]: http://reallysimpleworks.com/
[6]: http://www.famfamfam.com/lab/icons/silk/
[7]: http://p.yusukekamiyamane.com/
[8]: http://www.rgraph.net/

[_1]: http://dblp.cloudmining.net
[_2]: http://imdb.cloudmining.net
[_3]: http://medline.cloudmining.net

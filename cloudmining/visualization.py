"""This module is used to support different facet visualizations as pluggins.
Simply extend the Visualization class and then register it to your app:

app.register_visualization(YourVisualizationClass)
"""


class Visualization(object):
    """Extend this class to create new visualizations."""
    def __init__(self, app):
        self.app = app
        self.name = str(self.__class__.__name__).lower()
        self.description = self.name

    def setup(self, facet, **kwargs):
        """This will always be called before rendering the facet."""
        pass

    def render(self, computed_facet, **kwargs):
        """Renders the computed facet."""
        return self.app.view.facets.__getattr__(self.name)(computed_facet, **kwargs)


class TagCloud(Visualization):
    """A facet as a tag cloud."""
    def __init__(self, app):
        super(TagCloud, self).__init__(app)
        self.name = 'tag_cloud'
        self.description = 'tag cloud'


class Counts(Visualization):
    """A facet as a histogram count."""
    pass


class Rose(Visualization):
    """Uses RGraph to render the facet as a rose diagram."""
    def __init__(self, app):
        super(Rose, self).__init__(app)
        self.app.add_javascripts(
            '/js/rgraph/RGraph.common.core.js',
            '/js/rgraph/RGraph.common.tooltips.js',
            '/js/rgraph/RGraph.common.effects.js',
            '/js/rgraph/RGraph.rose.js'
        )

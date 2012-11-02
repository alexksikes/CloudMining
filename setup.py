#!/usr/bin/env python

from distutils.core import setup

long_description = '''
**Cloud Mining** is a exploratory search interface to the Sphinx_ retrieval 
engine. It uses fSphinx_ for the facets and SimSearch_ for item based search.

Here are some examples of instances powered by Cloud Mining: IMDb_ , DBLP_ or MEDLINE_.

.. _Sphinx: http://sphinxsearch.com
.. _IMDb: http://imdb.cloudmining.net
.. _DBLP: http://dblp.cloudmining.net
.. _MEDLINE: http://medline.cloudmining.net
'''

setup(name='CloudMining',
    version='0.5',
    description='Cloud Mining is a exploratory search interface to Sphinx.',
    author='Alex Ksikes',
    author_email='alex.ksikes@gmail.com',
    url='https://github.com/alexksikes/cloudmining/',
    download_url='https://github.com/alexksikes/cloudmining/tarball/master',
    packages=['cloudmining', 'cloudmining/app/controllers'],
    package_dir={'cloudmining': 'cloudmining'},
    package_data={'cloudmining': ['*.py']},
    long_description=long_description,
    license='AGPL'
)

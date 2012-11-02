#! /usr/bin/env python

import sys
import getopt

from cloudmining import CloudMiningApp
from fsphinx import FSphinxClient
from simsearch import SimClient


def run(fsphinx_config='', sim_config='', from_dir='', port='', no_debug=False):
    if fsphinx_config:
        cl = FSphinxClient.FromConfig(fsphinx_config)
    else:
        cl = None
    if sim_config:
        sim_cl = SimClient.FromConfig(sim_config)
    else:
        sim_cl = None
    if no_debug:
        autoreload = False
    else:
        autoreload = True
    if from_dir:
        app = CloudMiningApp.from_directory(from_dir, cl=cl, sim_cl=sim_cl, autoreload=autoreload)
    else:
        app = CloudMiningApp(cl, sim_cl, autoreload=autoreload)
    if port:
        app.set_port(port)
    if no_debug:
        app.debug = False
        app.template_caching = True
    app.run()


def usage():
    print 'Usage:'
    print '    python serve.py [options]'
    print
    print 'Description:'
    print '    Create a Cloud Mining web app from specified config files.'
    print
    print 'Options:'
    print '    -c, --fsphinx <fsphinx_config>  : path to sphinx config file'
    print '    -s, --sim <sim_config>          : path to simsearch config'
    print '    --from-dir <path>               : make app from directory'
    print '    -p, --port <number>             : port number'
    print '    --no-debug                      : no autoreload, template caching and no debug error'
    print '    -h, --help                      : this help message'
    print
    print 'Email bugs/suggestions to Alex Ksikes (alex.ksikes@gmail.com)'


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'c:s:p:h',
            ['fsphinx=', 'sim=', 'from-dir=', 'port=', 'no-debug', 'help'])
    except getopt.GetoptError:
        usage(); sys.exit(2)

    fsphinx_config, sim_config, port = '', '', 8080
    no_debug, from_dir = False, ''
    for o, a in opts:
        if o in ('-c', '--fsphinx'):
            fsphinx_config = a
        elif o in ('-s', '--sim'):
            sim_config = a
        elif o == '--from-dir':
            from_dir = a
        elif o in ('-p', '--port'):
            port = int(a)
        elif o == '--no-debug':
            no_debug = True
        elif o in ('-h', '--help'):
            usage(); sys.exit()

    if not opts:
        usage()
    else:
        run(fsphinx_config, sim_config, from_dir, port, no_debug)

if __name__ == '__main__':
    main()

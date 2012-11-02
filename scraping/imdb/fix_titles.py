# Author: Alex Ksikes

import sys
import codecs
from html import strip_html

def clean(s):
    return strip_html(s.strip('"')).strip()

def run(titles):
    for l in codecs.open(titles, encoding='utf8'):
        r = l.split('\t')
        try:
            r = map(clean, r)
        except:
            print >> sys.stderr, l.encode('utf8')
        print '\t'.join(r).encode('utf8')
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: python fix_titles.py titles.tbl'
    else:
        print run(sys.argv[1])

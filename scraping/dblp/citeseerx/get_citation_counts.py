'''
To use you need to set some environ variables for the database parameters:

    export dbn=mysql db=database user=user passwd=passwd
'''

import os
import re
import sys
import web

p = re.compile('\w+', re.I|re.U)
def make_key(title):
    return ''.join(p.findall(title)).strip().lower()

def load(counts_list):
    _counts = {}
    for counts in counts_list[::-1]:    
        for i, l in enumerate(open(counts)):
            (md5, cid, title, count) = l.split('\t')
            key = make_key(title)
            if key:
                _counts[key] = (count.strip(), cid)
            # if i % 10000 == 0:
            #     sys.stderr.write('%s\n' % i)
    return _counts

def get_db_params_from_env():
    return dict((k, v) for k, v in os.environ.items() 
        if k in ('dbn', 'db', 'user', 'passwd'))

def run(counts):
    db = web.database(**get_db_params_from_env())

    counts = load(counts)
    # import ipdb; ipdb.set_trace()
    
    for r in db.select('pub', what='id, title'):
        key = make_key(r.title)
        r.title = r.title.encode('utf-8')
        if key in counts:
            count, cid = counts[key]
            print '\t'.join([str(r.id), r.title, count, cid])
#        else:
#            sys.stderr.write('NO COUNT: %s\n' % r.title)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python get_citation.py counts.txt ..."
        print
        print "Can take multiple count files in order to keep the previous"
        print "scrape if it is not found in the new scrape (from newer to older)."
    else:
        run(sys.argv[1:])

import sys; sys.path.insert(0, '.')
import re

from config import db

p = re.compile('\w+', re.I|re.U)
def make_key(title):
    return ''.join(p.findall(title)).strip().lower()

def load(counts):
    _counts = {}
    for i, l in enumerate(open(counts)):
        (count, cid, title) = l.split('\t')
        _counts[make_key(title)] = (count, cid)
#        if i % 10000 == 0:
#            sys.stderr.write('%s\n' % i)
    return _counts

def run(counts):
    counts = load(counts)
    import ipdb; ipdb.set_trace()
    
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
        print "Usage: python get_citation.py file_counts"
    else:
        run(sys.argv[1])

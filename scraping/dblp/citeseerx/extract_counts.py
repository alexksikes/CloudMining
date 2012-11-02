import sys, re

p = re.compile('"citation\scount">(\d+)</em>.*?cid=(\d+)"><em>(.+?)</em></a>', re.I)
def run(file):
    for l in open(file):
        for m in p.findall(l):
            print '\t'.join(m)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python extract_counts.py file"
    else:
        run(sys.argv[1])
        
# then run as follow: find /projects/data/dblp/citeseerx/* -type f -exec python extract_counts.py {} \; > counts.txt
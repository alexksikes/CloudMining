import os
import re
import sys

# p = re.compile('"citation\scount">(\d+)</em>.*?cid=(\d+)"><em>(.+?)</em></a>', re.I)
p = re.compile('="bibcite">.*?cid=(\d+)">(.*?)</a>.*?="cites">(\d+)</div>', re.S)

def run(file):
    html = open(file).read()
    for m in p.findall(html):
        print '\t'.join((os.path.basename(file),) + m)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python extract_counts.py html_file"
    else:
        run(sys.argv[1])
        
# then run as follow: find /projects/data/cloudmining/dblp/citeseerx/html/* -type f -exec python extract_counts.py {} \; > counts.txt &
import sys

def run(max_year):
    # years from 1990 to 2013
    for year in range(1990, max_year):
       for start in range(0, 10000, 100):
           print 'http://citeseerx.ist.psu.edu/stats/articles?t=articles&y=%s&st=%s' % (year, start)

    # all years even less than 1990
    for start in range(0, 10000, 100):
        print 'http://citeseerx.ist.psu.edu/stats/articles?t=articles&st=%s' % start
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python get_urls.py max_year"
    else:
        run(int(sys.argv[1]))
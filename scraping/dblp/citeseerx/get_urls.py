#for year in range(1990, 2012):
#    for start in range(0, 10000, 100):
#        print 'http://citeseerx.ist.psu.edu/stats/articles?t=articles&y=%s&st=%s' % (year, start)

# citeseer only provides years from 1990 - 2012
# But provides data for all years (even < 1990). 
# Articles must have a least 65 citations.
for start in range(0, 10000, 100):
    print 'http://citeseerx.ist.psu.edu/stats/articles?t=articles&st=%s' % start

import sys
import re
import web

db = web.database(dbn='mysql', db='medline', user='ale', passwd='3babes')

def generate_pmc_urls():
    for r in db.select('citations', what='pmid, pmc_id', where='pmc_id is not NULL'):
        print 'http://www.ncbi.nlm.nih.gov/pmc/articles/PMC%s/' % r.pmc_id
            
if __name__ == '__main__':
    if len(sys.argv) < 1:
        print "Usage: python generate_pmc_urls.py mesh.tbl"
        print
        print "Description: Return a list of PMC urls."
    else:
        generate_pmc_urls()
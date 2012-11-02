import sys
import re

def get_mesh_terms(path):
    f = open(path)
    print f.readline().strip()
    
    for l in f:
        filename, pmid, mesh = l.strip().split('\t')
        for m in mesh.split('/'):
            print '%s\t%s\t%s' % (filename, pmid, re.sub('^\*', '', m)) 
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python get_mesh_terms.py mesh.tbl"
        print
        print "Description: The get Mesh terms as filename pmid mesh from mesh.tbl"
    else:
        get_mesh_terms(sys.argv[1])
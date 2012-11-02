# Author: Alex Ksikes (alex.ksikes@gmail.com)

import time
import sys
import md5
import os
import random

def make_file_md5(filename):
    return md5.new(filename).hexdigest()

def wget_dnl_cookie():
    url = 'http://www.ncbi.nlm.nih.gov/sites/pubmed?EntrezSystem2.PEntrez.DbConnector.Term=english'
    cmd = 'wget -O tmp --cookies=on --keep-session-cookies --save-cookies=cookie.txt "%s"' % url
    os.system(cmd)
    
def wget_dnl(url, out):
    cmd = 'wget -O %s --cookies=on --load-cookies=cookie.txt --keep-session-cookies "%s"' % (out, url)
    os.system(cmd)
    
def shuffle_urls(urls):
    urls = [url.strip() for url in open(urls)]
    random.shuffle(urls)
    return urls
        
def dnl_medline(urls, out_dir, delay=1):
    wget_dnl_cookie()
    
    for url in shuffle_urls(urls):
        fmd5 = make_file_md5(url)
        out = os.path.join(out_dir, fmd5)
        
        time.sleep(delay)
        wget_dnl(url, out)
        
        sys.stdout.flush()
        print url + '\t' + fmd5

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: python dnl_medline.py list_of_urls out_dir [delay in sec]"
    else:
        delay = len(sys.argv) > 3 and int(sys.argv[3]) or 1
        dnl_medline(sys.argv[1], sys.argv[2], delay)
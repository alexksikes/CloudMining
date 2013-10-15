Here is how to get the citation counts from [CiteSeerX](http://citeseerx.ist.psu.edu/stats/articles).

1) Get a list of urls to download from (at this time year is 2013):

    python get_urls.py 2013 > urls

2) Use retrieve.py from [Mass Scraping](https://github.com/alexksikes/mass-scraping) to download the urls:

    nohup retrieve.py -sc 4 -o /projects/data/cloudmining/dblp/citeseerx/html/ urls > urls.dnl &

3) Parse the downloaded html and extract the citation counts:

    find /projects/data/cloudmining/dblp/citeseerx/html/* -type f -exec python extract_counts.py {} \; > counts.txt &

Note you may have to update the regex in extract_counts.py.

4) Match SQL ids with article title:
    
    export dbn=mysql db=dblp user=your_username passwd=your_password
    nohup python get_citation_counts.py counts.txt counts.2011.txt > citation_counts.txt &

Note that some articles are not properly matched due to improper formatting from CiteSeerX. In this case we can keep the previous scrape by adding other count files (from newer to older). Here we are adding a scrape from 2011.

5) Clean up:

    unset dbn db user passwd
    mv urls* *.txt /projects/data/cloudmining/dblp/citeseerx/
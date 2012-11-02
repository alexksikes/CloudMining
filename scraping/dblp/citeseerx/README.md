We get the citation counts from citeseerx: http://citeseerx.ist.psu.edu/stats/articles

1) Get a list of urls to donwload from:

python get_urls.py > urls

2) Use retriever.py from Mass Scrapping to download the urls:

nohup retrieve.py -sc 4 -o /projects/data/dblp/citeseerx/ urls > urls.dnl &

3) Parse the downloaed html and extract the citation counts:

find /projects/data/dblp/citeseerx/ -type f -exec python extract_counts.py {} \; > counts.txt

4) Match SQL ids with article title

nohup python script/citeseerx/get_citation_counts.py scripts/citeseerx/counts.txt > scripts/citeseerx/citation_counts.txt &

5) Load into MySQL:

load data infile '/projects/scripts/dblp/script/citeseerx/citation_counts.txt' into table citeseerx_citations (id, @dummy, counts, cid);

We forgot to do so with all years merged http://citeseerx.ist.psu.edu/stats/articles?t=articles&st=100, that's why some files have the suffixe all_years.

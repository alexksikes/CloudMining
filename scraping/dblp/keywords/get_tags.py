# Author: Alex Ksikes

# Note:
# run python scripts/get_tags.py scripts/stopwords.txt pub title &
# cut -f 1,3 tag_freqs.txt > freqs.txt
# python scripts/get_tags.py scripts/stopwords.txt pub title freqs.txt&

import sys; sys.path.insert(0, '.')

import web
from config import db

from tagger import StopListTagger

def run(stop_words, table, field, freq_list=''):
    tag_ids = {}; tag_counts = {}
    
    out = open('tag_%s_%s.txt' % (table, field), 'w')
    out_tags = open('tag_ids.txt', 'w')
    out_freqs = open('tag_freqs.txt', 'w')
    
    tagger = StopListTagger(stop_words, freq_list)
    tag_id = 0
    for row in db.select(table, what='id, %s' % field):
        for tag in tagger.tag(row[field]):
            if tag not in tag_ids:
                tag_id +=1
                tag_ids[tag] = tag_id
                out_tags.write('%s\t%s\n' % (tag_ids[tag], tag.encode('utf8')))
                
            web.dictincr(tag_counts, tag)
            out.write('%s\t%s\t%s\t%s\n' % (row.id, row[field].encode('utf8'), tag.encode('utf8'), tag_ids[tag]))
        
    for tag in sorted(tag_counts, key=lambda x: tag_counts[x], reverse=True):
        out_freqs.write('%s\t%s\t%s\n' % (tag.encode('utf8'), tag_ids[tag], tag_counts[tag]))
    
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Usage: python get_tags.py stop_list mysql_table mysql_field [freqency_list]'
    else:
        print run(*sys.argv[1:])

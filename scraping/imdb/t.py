#| filename         | varchar(32)      | YES  |     | NULL    |       |
#| imdb_id          | int(12) unsigned | NO   | PRI |         |       |
#| title            | varchar(250)     | YES  |     | NULL    |       |
import sys, re

s = ''
for l in open(sys.argv[1]):
    print l.split('|')[1].strip() + ',',

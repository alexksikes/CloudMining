__author__ = 'Alex Ksikes <alex.ksikes@gmail.com>'

import re
import web
import math


class Expose(object):
    def __init__(self, name, sql_table, max_size=1000, **kwargs):
        self.name = name
        self.sql_table = sql_table
        self.max_size = max_size
        self.sql_field = kwargs.get('sql_field', 'name')
        self.sql_id = kwargs.get('sql_id', 'id')
        self.count = db.query('select count(*) as c from %s' % sql_table)[0].c
        self.set_location('/')

    def set_location(self, path):
        ppath = re.findall('/?(\d+)-(\d+)/?', path)
        if path == '/':
            start_id = 1
            end_id = self.count
        elif not ppath:
            start_id = 0
            end_id = 0
        else:
            start_id, end_id = map(int, ppath[-1])

        size = end_id - start_id + 1

        step = size / (self.max_size - 1)
        if step <= self.max_size:
            step = int(math.sqrt(size))

        self.start_id = start_id
        self.end_id = end_id
        self.step = step
        self.size = size
        self.path = path
        self.ppath = ppath

    def __iter__(self):
        if self.is_listing_entries():
            return self.list_entries()
        else:
            return self.list_ranges()

    def is_listing_entries(self):
        return self.size <= self.max_size

    def list_entries(self):
        return (a for a in db.select(self.sql_table,
            vars = dict(start_id=self.start_id, end_id=self.end_id),
            what = 'id, %s as value' % self.sql_field,
            where = 'id >= $start_id and id <= $end_id',
            limit = self.max_size))

    def list_ranges(self):
        r = db.select(self.sql_table,
            vars = dict(start_id=self.start_id, end_id=self.end_id, step=self.step),
            what = 'id, %s as value' % self.sql_field,
            where = 'id >= $start_id and id <= $end_id and\
                    ((id-$start_id) % $step = 0 or (id-$start_id+1) % $step = 0 or\
                     id = $end_id)',
            limit = self.max_size * 2)
        return web.group(r, 2)

    def extend_path(self, root='/', start_id='', end_id=''):
        url = '/%s/%s/%s-%s' % (root, self.path, start_id, end_id)
        return re.sub('/{2,}', '/', url)

    def get_by_id(self, id):
        return db.select(self.sql_table,
            vars = dict(id=id),
            what = 'id, %s as value' % self.sql_field,
            where = 'id=$id')[0]

    def get_breadcrumb(self):
        return [(self.get_by_id(id1), self.get_by_id(id2)) for id1, id2 in self.ppath]

#def make_index_table(db, src_tbl, src_fld, drop=False):
#    tbl = '%s_idx' % src_fld
#
#    if drop:
#        vars = dict(tbl=tbl),
#        db.query('drop table if exists $tbl')
#
#    db.query(
#        vars = dict(tbl=src_tbl, fld=src_fld),
#        'alter table $tbl add index($fld)'
#    )
#
#    db.query(
#        vars = dict(tbl=tbl, fld=src_fld),
#        'create table $tbl ('
#        '    id                      int(32) unsigned primary key auto_increment,'
#        '    $fld                 varchar(70) not null,'
#        '    index($fld)'
#        ') charset utf8 engine MyISAM')
#
#    db.query(
#        vars = dict(tbl=tbl, src_tbl=src_tbl, fld=src_fld),
#        'insert $tbl'
#        '    select $fld'
#        '    from $src_tbl'
#        '    where $fld is not NULL '
#        'group by $fld '
#        'order by $fld')

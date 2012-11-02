# inspired from webpy template reader

__author__ = 'Alex Ksikes <alex.ksikes@gmail.com>'

import glob
import os

try:
    from web.template import Template
except ImportError, e:
    Template = None


def file_reader(path):
    return open(path).read()


def template_reader(path, **keywords):
    if Template:
        return Template(open(path).read(), filename=path, **keywords)
    return file_reader(path)

READERS = {
    '*': file_reader,
    '.html': template_reader
}


class DirectoryMapper:
    def __init__(self, loc='.', cache=None, readers=READERS):
        self._loc = [loc]
        self._readers = readers
        if cache:
            self._cache = {}
        else:
            self._cache = None
        self._sub_dirs = {}

    def _map(self, loc, pos=0):
        loc = os.path.realpath(loc)
        if loc in self._loc:
            self._unmap(loc)
        self._loc.insert(pos, loc)

    def _unmap(self, loc):
        self._loc.remove(os.path.realpath(loc))

    def _list(self):
        print self

    def _lookup(self, name, pos=0):
        if pos >= len(self._loc):
            return 'none', None

        path = os.path.join(self._loc[pos], name)
        if os.path.isdir(path):
            return 'dir', path
        else:
            path = self._findfile(path)
            if path:
                return 'file', path
            else:
                return self._lookup(name, pos + 1)

    def _read(self, name, reader=None):
        kind, path = self._lookup(name)
        if kind == 'dir':
            if path not in self._sub_dirs:
                self._sub_dirs[path] = DirectoryMapper(path,
                    cache=self._cache is not None, readers=self._readers)
            return self._sub_dirs[path]
        elif kind == 'file':
            if not reader:
                ext = os.path.splitext(path)[-1]
                if ext in self._readers:
                    reader = self._readers[ext]
                else:
                    reader = self._readers.get('*', file_reader)
            return reader(path, **reader.func_dict.get('keywords', {}))
        else:
            raise AttributeError('No file named ' + name)

    def _findfile(self, path_prefix):
        p = [f for f in glob.glob(path_prefix + '*')]
        p.sort()  # sort the matches for deterministic order
        return p and p[0]

    def __getitem__(self, name):
        if os.path.sep in name:
            names = os.path.normpath(name).split(os.path.sep)
            result = self.__getattr__(names[0])
            for name in names[1:]:
                result = result.__getitem__(name)
            return result
        return self.__getattr__(name)

    #!FIX: gets called multiple times
    def __getattr__(self, name):
        if self._cache is not None:
            if name not in self._cache:
                self._cache[name] = self._read(name)
            return self._cache[name]
        else:
            return self._read(name)

    def __lshift__(self, loc):
        self._map(loc, 0)

    def __rshift__(self, loc):
        self._map(loc, len(self._loc))

    def __repr__(self):
        return '<DirectoryMapper\n%s >' % self

    def __str__(self):
        s = ''
        for loc in self._loc:
            if s:
                s += '\n'
            s += '* %s\n' % loc
            s += '    - ' + '\n    - '.join(
                os.path.isdir(os.path.join(loc, f)) and f + '/' or f
                    for f in os.listdir(loc))
        return s

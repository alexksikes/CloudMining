__author__ = 'Alex Ksikes <alex.ksikes@gmail.com>'

import datetime
import urlparse
import simplejson
import fnmatch
import urllib
import web
import imp
import os
import hashlib
import collections

json_encode = simplejson.dumps
urlunquote = urllib.unquote_plus


def homedomain():
    return web.ctx.get('homedomain', '')


def domain():
    return '.'.join(homedomain().split('.')[:-3:-1][::-1])


def how_long(d):
    return web.datestr(d, datetime.datetime.now())


def urlquote_plus(val, safe='/|*='):
    if val is None:
        return ''
    if not isinstance(val, unicode):
        val = str(val)
    else:
        val = val.encode('utf-8')
    return urllib.quote_plus(val, safe)


def url_encode2(inputs, clean=True, doseq=True, **kw):
    inputs = web.dictadd(inputs, kw)
    if clean is True:
        for q, v in inputs.items():
            if not v:
                del inputs[q]
            if isinstance(v, unicode):
                inputs[q] = v.encode('utf-8')
    return urllib.urlencode(inputs, doseq)


def cut_length(s, max=40):
    if len(s) > max:
        s = s[0:max] + '...'
    return s


def get_nice_url(url):
    host, path = urlparse.urlparse(url)[1:3]
    if path == '/':
        path = ''
    return cut_length(host + path)


def generate_md5(s):
    if not s:
        return None
    return hashlib.md5(s).hexdigest()


def get_inputs(**kwargs):
    inputs = web.input(**kwargs)
    return dict((i, inputs.get(i, kwargs[i])) for i in kwargs)


def url_parse(url):
    return web.storage(
        zip(('scheme', 'netloc', 'path', 'params', 'query', 'fragment'), urlparse.urlparse(url)))


def url_join(url, url_relative):
    if '://' not in url_relative:
        if not url_relative.startswith('/'):
            url_relative = '/' + url_relative
    return urlparse.urljoin(url, url_relative)


def get_user_ip():
    return web.ctx.get('ip', '000.000.000.000')


def dict_remove(d, *keys):
    for k in keys:
        if k in d:
            del d[k]


def get_extension_from_url(url):
    path = url_parse(url).path
    return path[path.rindex('.') + 1:]


def get_unique_md5():
    return hashlib.md5(str(datetime.datetime.now().microsecond)).hexdigest()


def get_guid():
    guid = get_unique_md5().upper()
    return '%s-%s-%s-%s-%s' % (guid[0:8], guid[8:12], guid[12:16], guid[16:20], guid[20:32])


def email_errors():
    if web.config.email_errors:
        web.emailerrors(web.config.email_errors, web.djangoerror())


def normalize(l, start=0, end=1):
    if not l:
        return l
    minl, maxl = min(l), max(l)
    return (1.0 * (end - start) * (x - minl) / ((maxl - minl) or 1) + start for x in l)


def pdberror():
    import sys
    try:
        import ipdb as pdb
    except ImportError:
        import pdb
    pdb.post_mortem(sys.exc_info()[2])
    return web.debugerror()


def path_to_module(module_path, name=''):
    if not name:
        name = os.path.basename(module_path.replace('.py', ''))
    return imp.load_source(name, module_path)


def filter_by_keys(l, key=None, keys=[]):
    if not key:
        key = lambda (x): x
    d = dict((key(v), v) for v in l)
    for k in keys:
        yield d[k]


def add_uniq(l, ele, key=None):
    key = key or (lambda x: x)
    if not isinstance(ele, collections.Iterable):
        ele = [ele]
    for e in ele:
        while e in l:
            l.remove(e)
        l.append(e)


def walkfiles(root_path, pattern='*'):
    for root, dirs, files in os.walk(root_path):
        for filename in fnmatch.filter(files, pattern):
            abspath = os.path.join(root, filename)
            yield web.storage(
                root=root,
                filename=filename,
                abspath=abspath,
                relpath=os.path.relpath(abspath, start=root)
            )

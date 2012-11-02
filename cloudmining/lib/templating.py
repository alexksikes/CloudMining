__author__ = 'Alex Ksikes <alex.ksikes@gmail.com>'

import re
import web
import utils


def public(f):
    """Exposes a function in templates. A list of functions or variables can
    also be supplied as dictionnary."""
    if isinstance(f, dict):
        web.template.Template.globals.update(f)
    else:
        web.template.Template.globals[f.__name__] = f

public(dict(
    # from web.http
    changequery = web.changequery,
    urlencode = web.http.urlencode,
    url = web.url,

    # from web.utils
    utf8 = web.utf8,
    strips = web.strips,
    rstrips = web.rstrips,
    lstrips = web.lstrips,
    group = web.group,
    listget = web.listget,
    intget = web.intget,
    datestr = web.datestr,
    numify = web.numify,
    denumify = web.denumify,
    commify = web.commify,
    nthstr = web.nthstr,
    cond = web.utils.cond,
    to36 = web.to36,
    safemarkdown = web.safemarkdown,

    # from web.net
    urlquote = web.urlquote,
    httpdate = web.httpdate,
    htmlquote = web.htmlquote,
    htmlunquote = web.htmlunquote,
    websafe = web.websafe,

    # more from webpy
    debug = web.debug,
    input = web.input,
    frender = web.template.frender,

    # common utilities
    int = int,
    str = str,
    list = list,
    set = set,
    dict = dict,
    min = min,
    max = max,
    range = range,
    len = len,
    repr = repr,
    zip = zip,
    isinstance = isinstance,
    enumerate = enumerate,
    hasattr = hasattr,
    sorted = sorted,
    sum = sum,
    getattr = getattr,

    # more utilities
    json_encode = utils.json_encode,
    urlunquote = utils.urlunquote,
    urlquote_plus = utils.urlquote_plus,
    how_long = utils.how_long,
    url_encode2 = utils.url_encode2,
    get_inputs = utils.get_inputs,
    cut_length = utils.cut_length,
    generate_md5 = utils.generate_md5
))


@public
def link(path, text=None):
    return '<a href="%s">%s</a>' % (web.ctx.homepath + path, text or path)


@public
def query_param(name, default=None):
    i = web.input(_m='GET')
    return i.get(name, default)


@public
def text2html(s):
    s = re.sub('\n', '<br />', s)
    s = re.sub('\t', 4 * ' ', s)
    return replace_links(s)


@public
def replace_links(s):
    return re.sub('(http://[^\s]+)', r'<a rel="nofollow" href="\1">' +
        utils.get_nice_url(r'\1') + '</a>', s, re.I)


@public
def split(pattern, str):
    return re.split(pattern, str)


@public
def wrap_tag(tag, _list):
    return ('<%s>%s</%s>' % (tag, e, tag) for e in _list)


@public
def change_params(**kwargs):
    return re.sub('/.*?\?', '', web.changequery(**kwargs))

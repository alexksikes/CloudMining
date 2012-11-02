import web
import re

from cloudmining.lib.templating import public


@public
def fix_pagination(s):
    if s is None:
        s = ''
    return web.listget(re.findall('^\w?[\d-]+', s), 0)


@public
def fix_author_initials(s):
    s = s.split()
    if len(s) > 1:
        s[-1] = s[-1].upper()
    return ' '.join(s)
import simplejson as json
import web

cookie_name = 'user_pref'


def get():
    pref = get_default()
    c = web.cookies().get(cookie_name, '{}')
    c = json.loads(c)
    pref.update(c)
    return pref


def reset():
    default = get_default()
    web.setcookie(cookie_name, json.dumps(default))
    return default


def get_default(as_module=True):
    defaults = {
        'highlighing': False,
        'sort_by': '',
        'selected_visu': {},
        'collapsed': {}, 
        'debug': False
    }
    for f in web.config.ui_facets:
        defaults['selected_visu'][f.name] = f.visualization
        defaults['collapsed'][f.name] = f.collapsed
    return defaults

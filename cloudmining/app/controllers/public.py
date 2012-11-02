import web
import mimetypes
import os

config = web.config


def mime_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


# this should not be called in production, serve statically
class public:
    def GET(self, type, filepath):
        web.header('Content-type', mime_type(os.path.basename(web.ctx.path)))
        return config.public['.' + web.ctx.path]  # check that!

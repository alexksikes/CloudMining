import web

urls = (
    '/hello', 'hello',    
)

class hello:    
    def GET(self):
        return 'hello world!'

class bye:
    def GET(self):
        return 'bye!'    

if __name__ == '__main__':
    #web.config.debug = False
    
    # keeping fvars=globals() won't do!
    #app = web.application(urls, fvars=globals())
    app = web.application(urls, dict(hello=hello))
    
    # explicitely specify fvars after adding mapping!
    app.add_mapping('/bye', 'bye')
    app.fvars['bye'] = bye
    
    # prints hello
    print app.request('/hello').data
    
    # not found unless web.config.debug = False 
    print app.request('/bye').data

# Instead explicitely specify fvars

#import web
#
#urls = (
#    '/hello', 'hello',    
#)
#
#class hello:    
#    def GET(self):
#        return 'hello world!'
#
#class bye:
#    def GET(self):
#        return 'bye!'    
#
#if __name__ == '__main__':
#    web.config.debug = False
#        
#    app = web.application(urls, fvars=dict(hello=hello))
#    
#    # adding the mapping for bye
#    app.add_mapping('/bye', 'bye')
#    #app.fvars['bye']=bye
#    
#    # prints hello
#    print app.request('/hello').data
#    
#    # not found unless web.config.debug = False 
#    print app.request('/bye').data

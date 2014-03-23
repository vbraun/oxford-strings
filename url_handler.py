from google.appengine.api import users


class BaseRequestHandler(webapp.RequestHandler):
    
    def initialize(self, request, response):
        webapp.RequestHandler.initialize(self, request, response)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
        from model import g_blog,User
        self.blog = g_blog
        self.login_user = users.get_current_user()

# -*- coding: utf-8 -*-
"""
App Request Handler
"""

import json
import webapp2
from webapp2 import cached_property
from google.appengine.api import users

from app import config
from app.page_model import Page

from markdown import markdown, extensions
from markdown.extensions.tables import TableExtension


json_encoder = json.JSONEncoder()


def jinja2_factory(app):
    from webapp2_extras import jinja2
    jinja_config = dict(jinja2.default_config)
    jinja_config['template_path'] = config.TEMPLATES_DIR
    j = jinja2.Jinja2(app, jinja_config)
    j.environment.filters.update({
    })
    j.environment.globals.update({
        'uri_for': webapp2.uri_for,
    })
    return j


class RequestHandler(webapp2.RequestHandler):

    @cached_property
    def jinja2(self):
        from webapp2_extras import jinja2
        return jinja2.get_jinja2(factory=jinja2_factory)
    
    def render_response(self, template, **kwds):
        kwds.setdefault('menu', config.menu_items)
        kwds.setdefault('path', self.request.path)
        kwds.setdefault('logged_in', bool(users.get_current_user()))
        kwds.setdefault('is_admin', users.is_current_user_admin())
        kwds.setdefault('login_url', users.create_login_url(self.request.uri))
        kwds.setdefault('logout_url', users.create_logout_url(self.request.uri))
        result = self.jinja2.render_template(template, **kwds)
        self.response.write(result)

    def json_response(self, **kwds):
        result = json_encoder.encode(kwds)
        self.response.write(result)

    def cache_must_revalidate(self):
        self.response.headers['Cache-Control'] = \
            'must-revalidate'

    def cache_disable(self):
        self.response.headers['Cache-Control'] = \
            'no-cache, no-store, must-revalidate, pre-check=0, post-check=0'



class PageRequestHandler(RequestHandler):

    def markdown(self, source):
        return markdown(source, extensions=[TableExtension(configs={})])

    def load_page(self, name):
        return Page.load(name)

    def load_page_history(self, name, limit=10):
        return Page.query_name(name).fetch(limit)

    def save_page(self, name, source):
        user = users.get_current_user()
        user_name = user.email()
        return Page.create(name, source, user_name)
        

    def get_page_names(self):
        pass

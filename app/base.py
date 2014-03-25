# -*- coding: utf-8 -*-
"""
App Request Handler
"""

import json
import webapp2
from webapp2 import cached_property
from markdown import markdown, extensions
from markdown.extensions.tables import TableExtension

import config

from .page_model import Page


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
        result = self.jinja2.render_template(template, **kwds)
        self.response.write(result)

    def json_response(self, **kwds):
        result = json_encoder.encode(kwds)
        self.response.write(result)

    def markdown(self, source):
        return markdown(source, extensions=[TableExtension(configs={})])

    def cache_must_revalidate(self):
        self.response.headers['Cache-Control'] = \
            'must-revalidate'

    def cache_disable(self):
        self.response.headers['Cache-Control'] = \
            'no-cache, no-store, must-revalidate, pre-check=0, post-check=0'



class PageRequestHandler(RequestHandler):

    def load_page(self, name):
        return Page.load(name)

    def save_page(self, name, source):
        return Page.create(name, source)
        

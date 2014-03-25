# -*- coding: utf-8 -*-
"""
Main entry point
"""

import sys
import os
import config
sys.path.append(config.LIB_DIR)

import webapp2
from webapp2 import WSGIApplication, Route, uri_for
from google.appengine.api import users

from .base import PageRequestHandler
from .decorators import cached_property, requires_login, requires_admin


class WikiPage(PageRequestHandler):

    def get(self, name='index.html'):
        page = self.load_page(name)
        values = dict()
        values['logged_in'] = bool(users.get_current_user())
        values['is_admin'] = users.is_current_user_admin()
        values['name'] = name
        values['menu'] = config.menu_items
        values['content'] = self.markdown(page.source)
        values['edit_url'] = uri_for('editor', name=name)
        values['login_url'] = users.create_login_url(self.request.uri)
        values['logout_url'] = users.create_logout_url(self.request.uri)
        self.render_response('page.html', **values)
        self.response.md5_etag()
        self.cache_must_revalidate()


class Editor(PageRequestHandler):
    
    @requires_admin
    def get(self, name):
        page = self.load_page(name)
        values = dict()
        values['name'] = name
        values['source'] = page.source
        values['preview'] = self.markdown(page.source)
        self.cache_disable()
        self.render_response('editor.html', **values)

    @requires_admin
    def post(self, name):
        command = self.request.get('command')
        source = self.request.get('source')
        if command == 'preview':
            html = self.markdown(source)
            self.json_response(ok=True, html=html)
        elif command == 'save':
            html = self.markdown(source)
            self.save_page(name, source)
            wiki_page = uri_for('wiki-page', name=name)
            self.json_response(ok=True, redirect=wiki_page)
        elif command == 'cancel':
            page = uri_for('wiki-page', name=name)
            self.json_response(ok=True, redirect=page)
        else:
            self.json_response(ok=False)
            


application = webapp2.WSGIApplication([
    Route(r'/', WikiPage),
    Route(r'/<name:[^/]*\.html>', WikiPage, name='wiki-page'),
    Route(r'/edit/<name:[^/]*\.html>', Editor, name='editor'),
], debug=True)


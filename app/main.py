# -*- coding: utf-8 -*-
"""
Main entry point
"""

import sys
import os
import config
sys.path.append(config.LIB_DIR)

import webapp2
from webapp2 import WSGIApplication, Route, cached_property, uri_for
import jinja2
from .base import PageRequestHandler


class EditablePage(PageRequestHandler):

    def get(self, name='index.html'):
        print('get', name)
        page = self.load_page(name)
        values = dict()
        values['name'] = name
        values['logged_in'] = True
        values['menu'] = config.menu_items
        values['content'] = self.markdown(page.source)
        values['edit_url'] = uri_for('editor', name=name)
        self.render_response('page.html', **values)
        self.response.md5_etag()
        self.cache_must_revalidate()


class Editor(PageRequestHandler):
    
    def get(self, name):
        page = self.load_page(name)
        values = dict()
        values['name'] = name
        values['source'] = page.source
        values['preview'] = self.markdown(page.source)
        self.cache_disable()
        self.render_response('editor.html', **values)

    def post(self, name):
        command = self.request.get('command')
        source = self.request.get('source')
        if command == 'preview':
            html = self.markdown(source)
            self.json_response(ok=True, html=html)
        elif command == 'save':
            html = self.markdown(source)
            self.save_page(name, source)
            editable_page = uri_for('editable-page', name=name)
            self.json_response(ok=True, redirect=editable_page)
        elif command == 'cancel':
            page = uri_for('editable-page', name=name)
            self.json_response(ok=True, redirect=page)
        else:
            self.json_response(ok=False)
            


application = webapp2.WSGIApplication([
    Route(r'/', EditablePage),
    Route(r'/<name:[^/]*\.html>', EditablePage, name='editable-page'),
    Route(r'/edit/<name:[^/]*\.html>', Editor, name='editor'),
], debug=True)


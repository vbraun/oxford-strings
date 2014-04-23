# -*- coding: utf-8 -*-
"""
Editable (Wiki-like) Web Pages
"""

import sys
import os

from webapp2 import uri_for
from google.appengine.api import users

from app import config
from app.base_view import PageRequestHandler
from app.decorators import cached_property, requires_login, requires_admin



class WikiPage(PageRequestHandler):

    def get(self, name='index.html'):
        self.cache_must_revalidate()
        page = self.load_page(name)
        values = dict()
        values['content'] = self.markdown(page.source)
        values['edit_url'] = uri_for('editor', name=name)
        values['history_url'] = uri_for('history', name=name)
        self.render_response('wiki_page.html', **values)
        self.response.md5_etag()


class Editor(PageRequestHandler):
    
    @requires_admin
    def get(self, name):
        self.cache_disable()
        page = self.load_page(name)
        values = dict()
        values['name'] = name
        values['source'] = page.source
        values['preview'] = self.markdown(page.source)
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




def html_diff(filename, previous, current):
    from difflib import unified_diff
    delta = unified_diff(
        current.splitlines(), previous.splitlines(),
        filename, filename)
    return '\n'.join(line.rstrip() for line in delta)
    

class History(PageRequestHandler):
    
    class ChangeSet(object):
        def __init__(self, name, page, previous):
            self.diff = html_diff(name, page.source, previous.source)
            self.author = page.author
            self.date = page.date
        
    def compute_changesets(self, name, limit=10):
        pages = self.load_page_history(name, limit)
        diffs = []
        for i in range(len(pages)-1):
            delta = History.ChangeSet(name, pages[i], pages[i+1])
            diffs.append(delta)
        return tuple(diffs)

    def get(self, name):
        self.cache_must_revalidate()
        values = dict()
        values['name'] = name
        values['changesets'] = self.compute_changesets(name)
        self.render_response('history.html', **values)
            



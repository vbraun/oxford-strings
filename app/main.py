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
from .base import RequestHandler




content = """
Welcome
=======

subhead
-------

### subsubhead

Lorem ipsum. By default, block-level elements stretch to the width of
their containers. If the browser window is small, the block-level
elements shrink in other words, text inside the con- tents wraps
within the confines of the contents' shrinking walls. However, when
you use pixel units rather than percentages, the width of the columns
becomes fixed. Even as a browser window shrinks or expands, the column
widths remain fixed. To keep the width of the left column fixed while
enabling the main column to stretch, simply remove the width property
assigned to the body element

    blockquote
    123

lists: 

*   Red
*   Green
*   Blue
*   This is a list item with two paragraphs.

    This is the second paragraph in the list item. You're
only required to indent the first line. Lorem ipsum dolor
sit amet, consectetuer adipiscing elit.

*   Another item in the same list.

enumerated: 

1.  Bird
1.  McHale
1.  Parish

- - -

Tables:

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

"""



class EditablePage(RequestHandler):

    def get(self, name='index.html'):
        print('get', name)
        values = dict()
        values['name'] = name
        values['logged_in'] = True
        values['menu'] = config.menu_items
        values['content'] = self.markdown(content)
        values['edit_url'] = uri_for('editor', name=name)
        self.render_response('page.html', **values)


class Editor(RequestHandler):
    
    def get(self, name):
        values = dict()
        values['name'] = name
        values['source'] = content
        values['preview'] = self.markdown(content)
        self.render_response('editor.html', **values)

    def post(self, name):
        command = self.request.get('command')
        source = self.request.get('source')
        if command == 'preview':
            html = self.markdown(source)
            self.response.write(html)
        elif command == 'save':
            # TODO: save
            html = self.markdown(source)
            self.response.write(html)
        elif command == 'cancel':
            self.response.write(uri_for('editable-page', name=name))
        else:
            assert False

application = webapp2.WSGIApplication([
    Route(r'/', EditablePage),
    Route(r'/<name:[^/]*\.html>', EditablePage, name='editable-page'),
    Route(r'/edit/<name:[^/]*\.html>', Editor, name='editor'),
], debug=True)


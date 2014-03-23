# -*- coding: utf-8 -*-

import sys
import os
import webapp2
from webapp2 import WSGIApplication, Route, cached_property, uri_for
import jinja2

from menu import menu_items


APP_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(APP_DIR, 'templates')
CSS_DIR = os.path.join(APP_DIR, 'static', 'css')
JS_DIR = os.path.join(APP_DIR, 'static', 'js')
LIB_DIR = os.path.join(APP_DIR, 'lib')

sys.path.append(LIB_DIR)
from markdown import markdown, extensions
from markdown.extensions.tables import TableExtension



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




def jinja2_factory(app):
    from webapp2_extras import jinja2
    config = dict(jinja2.default_config)
    config['template_path'] = TEMPLATES_DIR
    j = jinja2.Jinja2(app, config)
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



class EditablePage(RequestHandler):

    def get(self, name='index.html'):
        print('get', name)
        values = dict()
        values['logged_in'] = True
        values['menu'] = menu_items
        values['content'] = markdown(content, extensions=[TableExtension(configs={})])
        values['edit_url'] = uri_for('editor', name=name)
        self.render_response(name, **values)


class Editor(RequestHandler):
    
    def get(self, name):
        values = dict()
        values['name'] = name
        self.render_response('editor.html', **values)



application = webapp2.WSGIApplication([
    Route(r'/', EditablePage),
    Route(r'/<name:[^/]*\.html>', EditablePage, name='editable-page'),
    Route(r'/edit/<name:[^/]*\.html>', Editor, name='editor'),
], debug=True)


# -*- coding: utf-8 -*-

import sys
import os
import webapp2
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

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


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


class MainPage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        values = dict()
        values['logged_in'] = True
        values['menu'] = menu_items
        values['content'] = markdown(content, extensions=[TableExtension(configs={})])
        values['edit_url'] = 'edit?index.html'
        self.response.write(template.render(values))



application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)


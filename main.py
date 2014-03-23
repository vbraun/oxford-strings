# -*- coding: utf-8 -*-

import os
import webapp2
import jinja2

from menu import menu_items


APP_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(APP_DIR, 'templates')
CSS_DIR = os.path.join(APP_DIR, 'static', 'css')
JS_DIR = os.path.join(APP_DIR, 'static', 'js')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATES_DIR),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



class MainPage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        values = dict()
        values['logged_in'] = True
        values['menu'] = menu_items
        self.response.write(template.render(values))



application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)


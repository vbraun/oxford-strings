# -*- coding: utf-8 -*-
"""
Main entry point
"""


import sys
import os

from webapp2 import WSGIApplication, Route, uri_for
from google.appengine.api import users

from app.base_view import PageRequestHandler
from app.editable_view import WikiPage, Editor, History
from app.calendar_view import Seminars

application = WSGIApplication([
    Route(r'/', WikiPage),
    Route(r'/<name:[^/]*\.html>', WikiPage, name='wiki-page'),
    Route(r'/edit/<name:[^/]*\.html>', Editor, name='editor'),
    Route(r'/history/<name:[^/]*\.html>', History, name='history'),
    Route(r'/cal/seminars.html', Seminars, name='seminars'),
], debug=True)


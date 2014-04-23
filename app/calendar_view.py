# -*- coding: utf-8 -*-
"""
Calendaring Page Views
"""

import sys
import os

from webapp2 import uri_for
from google.appengine.api import users

import app.config as config
from app.base_view import RequestHandler
from app.decorators import cached_property, requires_login, requires_admin



class EventListing(RequestHandler):

    def get(self):
        self.cache_must_revalidate()
        values = dict()
        # values['name'] = name
        # values['edit_url'] = uri_for('calendar-edit')
        self.render_response('calendar.html', **values)
        self.response.md5_etag()



class Seminars(EventListing):
    pass
    

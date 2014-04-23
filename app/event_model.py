# -*- coding: utf-8 -*-
"""
Data model for calendar events
"""

from google.appengine.ext import ndb


class Event(ndb.Model):
    """
    A seminar
    """
    uid = ndb.StringProperty()
    sha1 = ndb.TextProperty()

    active = ndb.BooleanProperty()

    start_date = ndb.DateTimeProperty()
    end_date = ndb.DateTimeProperty()
    author = ndb.StringProperty(required=False, indexed=False)
    
    location= ndb.TextProperty(required=False)
    speaker = ndb.TextProperty(required=False)
    description = ndb.TextProperty(required=False)
    

# -*- coding: utf-8 -*-
"""
Data model for calendar events
"""

from webapp2 import uri_for
from google.appengine.ext import ndb


class Event(ndb.Model):
    """
    A seminar
    """
    uid = ndb.StringProperty()

    editable = ndb.BooleanProperty()
    active = ndb.BooleanProperty()

    start_date = ndb.DateTimeProperty()
    end_date = ndb.DateTimeProperty()
    author = ndb.StringProperty(required=False, indexed=False)
    
    location= ndb.TextProperty(required=False)
    speaker = ndb.TextProperty(required=False)
    title = ndb.TextProperty(required=False)
    description = ndb.TextProperty(required=False)
    


    def get_time(self):
        length = (self.end_date - self.start_date).seconds / 60
        return '{0} ({1} min)'.format(self.start_date, length)

    def get_edit_url(self):
        return uri_for('calendar-edit', uid=self.uid)

    def get_delete_url(self):
        return uri_for('calendar-remove', uid=self.uid)


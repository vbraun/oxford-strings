# -*- coding: utf-8 -*-
"""
Data model for calendar events
"""

from webapp2 import uri_for
from google.appengine.ext import ndb

from datetime import datetime
import time
import pytz
UTC_TZ = pytz.utc
LOCAL_TZ = pytz.timezone('Europe/London')


class Event(ndb.Model):
    """
    A seminar

    .. note::

        All times are stored as UTC
    """
    # The event unique id
    uid = ndb.StringProperty()

    editable = ndb.BooleanProperty()
    active = ndb.BooleanProperty()

    start_date = ndb.DateTimeProperty()
    end_date = ndb.DateTimeProperty()
    author = ndb.StringProperty(required=False, indexed=False)
    
    # The seminar series
    series = ndb.StringProperty(required=False)
    location= ndb.TextProperty(required=False)
    speaker = ndb.TextProperty(required=False)
    title = ndb.TextProperty(required=False)
    description = ndb.TextProperty(required=False)
    


    def get_time(self):
        delta = (self.start_date - datetime.utcnow()).days
        same_week = delta >= 0 and delta < 7
        t0 = self._to_localtime(self.start_date)
        if same_week:
            return time.strftime('%A at %H:%M', t0.timetuple())
        else:
            return time.strftime('%A, %B %e, at %H:%M', t0.timetuple())

    def get_time_short(self):
        t0 = self._to_localtime(self.start_date)
        return time.strftime('%b %e, %H:%M', t0.timetuple())

    def get_duration(self):
        length = (self.end_date - self.start_date).seconds / 60
        if length > 0:
            return '({} min)'.format(length)
        else:
            return ''

    def get_where(self):
        if self.location:
            return 'in {}'.format(self.location)
        else:
            return ''

    def get_edit_url(self):
        return uri_for('calendar-edit', uid=self.uid)

    def get_delete_url(self):
        return uri_for('calendar-remove', uid=self.uid)


    def _to_localtime(self, dt):
        """
        Convert to the local time
        """
        return UTC_TZ.localize(dt).astimezone(LOCAL_TZ)

    def _to_utc(self, dt):
        """
        Convert to the local time
        """
        return LOCAL_TZ.localize(dt).astimezone(UTC_TZ)

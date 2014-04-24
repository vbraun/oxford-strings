# -*- coding: utf-8 -*-
"""
Calendaring Page Views
"""

import sys
import os
import uuid
from datetime import datetime

from webapp2 import uri_for
from google.appengine.api import users

import app.config as config
from app.base_view import RequestHandler
from app.decorators import cached_property, requires_login, requires_admin
from app.event_model import Event
from app.ical import CalendarSync

class IcalSyncer(RequestHandler):

    def get(self):
        print 'sync'
        cal = CalendarSync()
        cal.import_file('/home/vbraun/Code/GAE/OxfordStrings/app/test/calendar/oxford.ics')
        cal.import_file('/home/vbraun/Code/GAE/OxfordStrings/app/test/calendar/google.ics')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(str(cal.events))


class CalendarEdit(RequestHandler):
    
    def get_event(self, uid):
        if uid is not None:
            ev = Event.query(Event.uid == uid).fetch(1)
            if len(ev) > 0:
                return ev[0]
        uid = str(uuid.uuid4())
        ev = Event(uid=uid, editable=True, active=True)
        ev.start_date = datetime.utcnow()
        ev.end_date = datetime.utcnow()
        ev.put()
        return ev

    def get(self, uid=None):
        values = dict()
        values['calendar'] = [self.get_event(uid)]
        self.render_response('calendar.html', **values)


class CalendarRemove(RequestHandler):
    
    def post(self, uid):
        ev = Event.query(Event.uid == uid).fetch(1)
        if len(ev) == 0:
            return
        ev = ev[0]
        ev.active = False
        ev.put



class EventListing(RequestHandler):

    def get_events(self):
        return Event.query().order(-Event.start_date).fetch(20)

    def get(self):
        self.cache_must_revalidate()
        values = dict()
        # values['name'] = name
        values['edit_url'] = uri_for('calendar-new')
        values['sync_url'] = uri_for('cron-sync')
        values['calendar'] = self.get_events()
        self.render_response('calendar.html', **values)
        self.response.md5_etag()



class Seminars(EventListing):
    pass
    

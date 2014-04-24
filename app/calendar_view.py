# -*- coding: utf-8 -*-
"""
Calendaring Page Views
"""

import sys
import os
import uuid
from datetime import date, datetime, timedelta

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



class CalendarRemove(RequestHandler):
    
    def post(self, uid, active):
        ev = Event.query(Event.uid == uid).fetch(1)
        if len(ev) == 0:
            return
        ev = ev[0]
        ev.active = False
        ev.put


class CalendarAdmin(RequestHandler):
    
    def get_events(self):
        """
        Return all future events
        """
        now = datetime.combine(date.today(), datetime.min.time())
        return Event.query(Event.start_date >= now).order(Event.start_date).fetch(100)

    def get(self):
        values = dict()
        values['sync_url'] = uri_for('cron-sync')
        values['full_url'] = uri_for('calendar-admin')
        values['calendar'] = self.get_events()
        self.render_response('calendar_admin.html', **values)

        
    



class EventListing(RequestHandler):

    def get_events(self):
        """
        Return all future events
        """
        now = datetime.combine(date.today(), datetime.min.time())
        return Event.query(Event.start_date >= now).order(Event.start_date).fetch(100)

    def get_template(self):
        raise NotImplementedError

    def get(self):
        self.cache_must_revalidate()
        values = dict()
        # values['edit_url'] = uri_for('calendar-new')
        values['sync_url'] = uri_for('cron-sync')
        values['full_url'] = uri_for('calendar-admin')
        values['calendar'] = self.get_events()
        self.render_response(self.get_template(), **values)
        self.response.md5_etag()



class Seminars(EventListing):

    def get_template(self):
        return 'calendar.html'



class BagLunch(EventListing):

    def get_events(self):
        """
        Return all future events in the bag lunch series
        """
        now = datetime.combine(date.today(), datetime.min.time())
        query = Event.query(Event.series == 'Bag Lunch', Event.start_date >= now)
        return query.order(Event.start_date).fetch(100)

    def get_template(self):
        return 'bag_lunch.html'


class ThisWeek(EventListing):
    
    def get_template(self):
        return 'this_week.html'
    
    def get_events(self):
        today = date.today()
        last_sunday = today - timedelta(days=today.weekday() + 1)
        next_sunday = last_sunday + timedelta(weeks=1)
        t0 = datetime.combine(last_sunday, datetime.min.time())
        t1 = datetime.combine(next_sunday, datetime.max.time())
        # allow for week-spanning events would be ideally:
        # query = Event.query(Event.start_date <= t1, Event.end_date >= t0)
        # but inequality queries can currently be only on one property
        query = Event.query(Event.start_date >= t0, Event.start_date < t1)
        return query.order(Event.start_date).fetch(100)


class CalendarEdit(EventListing):
    """
    TODO
    """
    
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


# -*- coding: utf-8 -*-
"""
Calendaring Page Views
"""

import sys
import os
import uuid
import logging
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
        values['calendar_admin_url'] = self.request.uri
        values['calendar'] = self.get_events()
        self.render_response('calendar_admin.html', **values)

    def post(self):
        key_id = self.request.get('key_id')
        active = (self.request.get('active') == u'true')
        ev = Event.get_by_id(int(key_id))
        ev.active = active
        ev.put()
    



class EventListing(RequestHandler):

    def get_events(self):
        """
        Return all future events
        """
        now = datetime.combine(date.today(), datetime.min.time())
        query = Event.query(Event.start_date >= now, Event.active == True)
        return query.order(Event.start_date).fetch(100)

    def get_template(self):
        raise NotImplementedError

    def get(self):
        self.cache_must_revalidate()
        values = dict()
        # values['edit_url'] = uri_for('calendar-new')
        values['sync_url'] = uri_for('cron-sync')
        values['calendar_admin_url'] = uri_for('calendar-admin')
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
        query = Event.query(
            Event.series == 'Bag Lunch', 
            Event.start_date >= now,
            Event.active == True)
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
        query = Event.query(
            Event.start_date >= t0, 
            Event.start_date < t1, 
            Event.active == True)
        return query.order(Event.start_date).fetch(100)


class CalendarEdit(EventListing):
    """
    TODO: do we really want to edit events ourselves?
    """
    
    def get_event(self, key_id):
        if key_id is not None:
            return Event.get_by_id(int(key_id))
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


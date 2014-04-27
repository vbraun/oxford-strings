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




class CalendarAdmin(RequestHandler):
    
    def get_events(self):
        """
        Return all future events
        """
        now = datetime.combine(date.today(), datetime.min.time())
        return Event.query(Event.start_date >= now).order(Event.start_date).fetch(100)

    def get(self):
        self.cache_must_revalidate()
        values = dict()
        values['sync_url'] = uri_for('cron-sync')
        values['full_url'] = uri_for('calendar-admin')
        values['calendar_admin_url'] = self.request.uri
        values['calendar'] = self.get_events()
        self.render_response('calendar_admin.html', **values)

    @requires_admin
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



class IcalExport(EventListing): 

    def _ical_time(self, dt):
        import pytz
        import time
        dt = pytz.utc.localize(dt)
        return time.strftime('%Y%m%dT%H%M%SZ', dt.timetuple())

    def get(self):
        from icalendar import Calendar, Event, vCalAddress, vText
        cal = Calendar()
        cal.add('prodid', '-//Strings Oxford Calendaring//strings.ox.ac.uk//')
        cal.add('version', '2.0')
        cal.add('X-WR-CALNAME', 'Strings Oxford')
        for ev in self.get_events():
            event = Event()
            event['uid'] = vText(ev.uid)
            event['location'] = vText(ev.location)
            event['summary'] = ev.title
            event['dtstart'] = self._ical_time(ev.start_date)
            event['dtend'] = self._ical_time(ev.end_date)
            desc  = u'Speaker: {}\n'.format(ev.speaker)
            desc += u'Location: {}\n'.format(ev.location)
            desc += u'Series: {}\n'.format(ev.series)
            desc += ev.description
            event['description'] = vText(desc)
            cal.add_component(event)
        #self.response.headers['Content-Type'] = 'text/plain'
        self.response.headers['Content-Type'] = 'text/calendar'
        self.response.write(cal.to_ical())



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
    
    def get_start_date(self):
        """
        Return the date of the last Saturday
        """
        today = date.today()
        # today.weekday in {0, ..., 6} switches to "0" on Monday
        key_day = today + timedelta(days=2)   # we want to switch calendar on saturday
        return today - timedelta(days=key_day.weekday())

    def get_events(self):
        last_saturday = self.get_start_date()
        next_saturday = last_saturday + timedelta(weeks=1)
        t0 = datetime.combine(last_saturday, datetime.min.time())
        t1 = datetime.combine(next_saturday, datetime.max.time())
        # allow for week-spanning events would be ideally:
        # query = Event.query(Event.start_date <= t1, Event.end_date >= t0)
        # but inequality queries can currently be only on one property
        query = Event.query(
            Event.start_date >= t0, 
            Event.start_date < t1, 
            Event.active == True)
        return query.order(Event.start_date).fetch(100)


class NextWeek(ThisWeek):
    
    def get_template(self):
        return 'next_week.html'
    
    def get_start_date(self):
        """
        Return the date of the next Saturday
        """
        return ThisWeek.get_start_date(self) + timedelta(weeks=1)


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


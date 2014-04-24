"""
Utilities for ical files
"""



import re
import icalendar
import textwrap
import calendar
import time
from datetime import date, datetime
import urllib2


class IcalEvent(object):

    SPEAKER_RE = re.compile(u'^ *Speaker: *(.*)')
    LOCATION_RE = re.compile(u'^ *Location: *(.*)')

    def __init__(self, series, author, event, active_by_default=False):
        self.uid = event['UID']
        self.series = series
        self.author = author
        self.active_by_default = active_by_default
        self.start_date = self._utc(event['DTSTART'].dt)
        self.end_date = self._utc(event['DTEND'].dt)
        self.title = event.get('SUMMARY', 'No summary').replace('\n', '')
        self._init_description(event.get('DESCRIPTION', 'No description'))

    def _utc(self, dt):
        """
        Convert date to datetime UTC
        """
        if isinstance(dt, date):
            timestamp = time.mktime(dt.timetuple())
            dt = datetime.fromtimestamp(timestamp)
        return dt

    def _init_description(self, desc):
        self.location = ''
        self.speaker = ''
        self.description = ''
        for line in desc.splitlines():
            match = self.SPEAKER_RE.match(line)
            if match:
                self.speaker = match.group(1)
                continue
            match = self.LOCATION_RE.match(line)
            if match:
                self.location = match.group(1)
                continue
            self.description += line
        self.description = textwrap.dedent(self.description)

    def __repr__(self):
        s = u'Event\n'
        s += u'  unique id  : {}\n'.format(self.uid)
        s += u'  starts     : {}\n'.format(self.start_date)
        s += u'  ends       : {}\n'.format(self.end_date)
        s += u'  created by : {}\n'.format(self.author)
        s += u'  location   : {}\n'.format(self.location)
        s += u'  series     : {}\n'.format(self.series)
        s += u'  speaker    : {}\n'.format(self.speaker)
        s += u'  title      : {}\n'.format(self.title)
        s += u'  description: {}\n'.format(self.description)
        return s.encode('ascii', 'replace')
        
    def save(self):
        """
        Save to app engine datastore
        """
        from app.event_model import Event
        ev = Event.query(Event.uid == self.uid).fetch(1)
        if len(ev) == 0:
            ev = Event(uid=self.uid, editable=False, active=self.active_by_default)
        else: 
            ev = ev[0]
        ev.start_date = self.start_date
        ev.end_date = self.end_date
        ev.author = self.author
        ev.series = self.series
        ev.location = self.location
        ev.speaker = self.speaker
        ev.title = self.title
        ev.description = self.description
        ev.put()




class CalendarSync(object):

    def __init__(self):
        self.events = []

    def import_file(self, name, filename):
        with open(filename, 'r') as f:
            self.import_ical(name, f.read())
        
    def import_url(self, name, url, active_by_default=False):
        try:
            # ical = urllib2.urlopen(url).read()
            req  = urllib2.Request(url, None, {})    
            ical = urllib2.urlopen(req).read()
            print('urllib', ical)
            self.import_ical(name, ical, active_by_default)
        except urllib2.URLError, e:
            raise
        
    def import_ical(self, name, ical, active_by_default=False):
        cal = icalendar.Calendar.from_ical(ical)
        author = cal.get('X-WR-CALNAME', 'Unknown source').strip()
        for event in cal.subcomponents:
            event = IcalEvent(name, author, event, active_by_default)
            event.save()
            self.events.append(event)
            

            
            
# cal = CalendarSync()
# cal.import_file('/home/vbraun/Code/GAE/OxfordStrings/app/test/calendar/oxford.ics')
# cal.import_file('/home/vbraun/Code/GAE/OxfordStrings/app/test/calendar/google.ics')

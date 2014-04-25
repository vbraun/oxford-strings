# -*- coding: utf-8 -*-
"""
Configuration

All configuration goes into this file
"""

import os
import sys

# Set up paths. Only change this if you reorganize the project directory
APP_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(APP_DIR, 'templates')
CSS_DIR = os.path.join(APP_DIR, 'static', 'css')
JS_DIR = os.path.join(APP_DIR, 'static','js')
LIB_DIR = os.path.join(APP_DIR, 'lib')

# Ensure that LIB_DIR is exactly once in the search path
if LIB_DIR not in sys.path:
    sys.path.append(LIB_DIR)


# Edit this to change the menu. For anything that is not just an
# editable page (e.g. calendars) you have to change app/route.py as
# well.
from app.menu import MenuItem
menu_items = (
    MenuItem('Home',            '/index.html'),
    MenuItem('Members',         '/members.html'),
    MenuItem('Research',        '/research.html'),
    MenuItem('Seminars',        '/cal/seminars.html'),
    MenuItem('Bag lunch',       '/cal/bag_lunch.html', 1),
    MenuItem('This week',       '/cal/this_week.html', 1),
    MenuItem('Next week',       '/cal/next_week.html', 1),
    MenuItem('Graduate study',  '/graduates.html'),
)


# The calendars to pull from
from app.remote_calendars import Calendar
remote_calendars = (
    # series name, ical url, where to include events by default
    Calendar('String Theory', 'https://www.maths.ox.ac.uk/events/calendar/P2Y1D/4/930/ical', True),
    Calendar('Quantum Field Theory', 'http://www.maths.ox.ac.uk/events/calendar/P2Y1D/4/913/ical', True),
    Calendar('Geometry and Analysis', 'https://www.maths.ox.ac.uk/events/calendar/P2Y1D/4/886/ical', False),
    Calendar('Algebraic and Symplectic Geometry', 'https://www.maths.ox.ac.uk/events/calendar/P2Y1D/4/945/ical', False),
    Calendar('Number Theory', 'https://www.maths.ox.ac.uk/events/calendar/P2Y1D/4/903/ical', False),
    Calendar('Math Colloquium', 'https://www.maths.ox.ac.uk/events/calendar/P2Y1D/4/874/ical', True),
    Calendar('Bag Lunch', 'https://www.google.com/calendar/ical/bkhromh605bm44dl8fuq4dip58%40group.calendar.google.com/public/basic.ics', True),
)

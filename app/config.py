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
    MenuItem('Subscribe',       '/subscribe.html', 1),
    MenuItem('Graduate study',  '/graduates.html'),
)


# The calendars to pull from
# Note: the seminar series name can be overridden by a "Series: ..." line in the description
from app.remote_calendars import Calendar
remote_calendars = (
    # series name, ical url, where to include events by default
    Calendar('Math/Physics', 
             'https://p02-calendarws.icloud.com/ca/subscribe/1/H27V2KdwHOwU'
             'P1-T2utnLgUfT4rbXQwJ20lQlolSc7lxsTg7Rj7k8USjJdnX3fuPx6EX7bhjx'
             '6Lf87LvlFpnxEUmjjbFR6VG4uDCu8EBW08', True),
    Calendar('String Theory', 
             'https://www.maths.ox.ac.uk/events/calendar/P2Y1D/4/930/ical'),
    Calendar('Quantum Field Theory', 
             'http://www.maths.ox.ac.uk/events/calendar/P2Y1D/4/913/ical'),
    Calendar('Geometry and Analysis', 
             'https://www.maths.ox.ac.uk/events/calendar/P2Y1D/4/886/ical'),
    Calendar('Algebraic and Symplectic Geometry', 
             'https://www.maths.ox.ac.uk/events/calendar/P2Y1D/4/945/ical'),
    Calendar('Number Theory', 
             'https://www.maths.ox.ac.uk/events/calendar/P2Y1D/4/903/ical'),
    Calendar('Math Colloquium', 
             'https://www.maths.ox.ac.uk/events/calendar/P2Y1D/4/874/ical'),
    Calendar('Bag Lunch', 
             'https://www.google.com/calendar/ical/bkhromh605bm44dl8fuq4dip'
             '58%40group.calendar.google.com/public/basic.ics'),
    Calendar('Relativity', 
             'https://www.maths.ox.ac.uk/events/calendar/P2Y1D/4/915/ical'),
    Calendar('Physics', 
             'https://www2.physics.ox.ac.uk/ical/research/seminars'),
    Calendar('Twistor Workshop', 
             'https://www.maths.ox.ac.uk/events/calendar/P2Y1D/4/1837/ical'),
)

# Calendar sources (seminar series) whose events should be included by
# default. All others must be picked manually using the
# http://strings-oxford.appspot.com/cal/admin view.
default_series = (
    'String Theory',
    'Quantum Field Theory',
    'Math Colloquium',
    'Bag Lunch',
    'Holography Seminar',
    'Particle Phenomenology Forum',
    'Math/Physics',
    'Theoretical Physics Colloquium',
    'Algebraic and Symplectic Geometry',
    'Relativity',
    'Geometry and Analysis',
    'Particles and fields seminar',
    'Colloquia seminar',
    'Twistor Workshop',
)

default_series_lower_case = tuple(s.lower() for s in default_series)


# How to start the abstract.
abstract_intro = 'Further information:'

# The following will be stripped off if they are at the beginning of
# the abstract (case insensitive)
strip_abstract_intro = tuple(s.lower() for s in [
    abstract_intro,
    'more information:',
    'abstract:',
])
                             

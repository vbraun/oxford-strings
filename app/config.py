# -*- coding: utf-8 -*-
"""
Configuration

All configuration goes into this file
"""

import os
import sys

# Set up paths. Only change this if you reorganize the project directory
HOME_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATES_DIR = os.path.join(HOME_DIR, 'templates')
CSS_DIR = os.path.join(HOME_DIR, 'static', 'css')
JS_DIR = os.path.join(HOME_DIR, 'static','js')
LIB_DIR = os.path.join(HOME_DIR, 'lib')

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
    MenuItem('Junior seminar',  '/cal/junior_seminar.html', 1),
    MenuItem('This week',       '/cal/this_week.html', 1),
    MenuItem('Next week',       '/cal/next_week.html', 1),
    MenuItem('Subscribe',       '/subscribe.html', 1),
    MenuItem('Graduate study',  '/graduates.html'),
)


# This is the seminar name that is shown to the user
#
# The physics calendars all override their seminar name, so they don't
# actually appear under "Physics" but, e.g. "Holography Seminar".

seminar_names = {
    # Individual calendars that do not override their name, so we can
    # pick any name we like
    'math_phys': 'Math/Physics',
    'strings': 'String Theory Seminar',
    'qft': 'Quantum Field Theory Seminar',
    'geometry_analysis': 'Geometry and Analysis Seminar', 
    'algebraic_symplectic': 'Algebraic and Symplectic Geometry', 
    'number_theory': 'Number Theory Seminar', 
    'pde_seminar': 'PDE Seminar', 
    'math_colloquium': 'Math Colloquium', 
    'junior_strings': 'Strings Junior Seminar', 
    'relativity': 'Relativity Seminar', 
    'twistor': 'Twistor Workshop', 

    # Note: these are all physics calendars
    'all_of_physics': 'Physics', 

    # The remaining names must be exactly as they are named
    # in the physics calendar (up to case)
    'holography': 'Holography Seminar',
    'particle_pheno': 'Particle Phenomenology Forum',
    'theoretical_physics': 'Theoretical Physics Colloquia',
    'particles_and_fields': 'Particles and fields seminar',
    'physics_colloquia': 'Colloquia seminar',
}


# The calendars to pull from
#
# Note: the seminar series name can be overridden by a "Series: ..."
# line in the description

from app.remote_calendars import Calendar
remote_calendars = (
    # series name, ical url, where to include events by default
    #Calendar(seminar_names['math_phys'], 
    #         'https://p02-calendarws.icloud.com/ca/subscribe/1/H27V2KdwHOwU'
    #         'P1-T2utnLgUfT4rbXQwJ20lQlolSc7lxsTg7Rj7k8USjJdnX3fuPx6EX7bhjx'
    #         '6Lf87LvlFpnxEUmjjbFR6VG4uDCu8EBW08', True),
    Calendar(seminar_names['strings'], 
             'https://www.maths.ox.ac.uk/events/list/695/all/calendar.ics'),
    Calendar(seminar_names['qft'], 
             'https://www.maths.ox.ac.uk/events/list/686/all/calendar.ics'),
    Calendar(seminar_names['geometry_analysis'], 
             'https://www.maths.ox.ac.uk/events/list/641/all/calendar.ics'),
    Calendar(seminar_names['algebraic_symplectic'],
             'https://www.maths.ox.ac.uk/events/list/624/all/calendar.ics'),
    Calendar(seminar_names['number_theory'],
             'https://www.maths.ox.ac.uk/events/list/669/all/calendar.ics'),
    Calendar(seminar_names['pde_seminar'],
             'https://www.maths.ox.ac.uk/events/list/682/all/calendar.ics'),
    Calendar(seminar_names['twistor'],
             'https://www.maths.ox.ac.uk/events/list/701/all/calendar.ics'),
    Calendar(seminar_names['math_colloquium'],
             'https://www.maths.ox.ac.uk/events/list/632/all/calendar.ics'),
#    Calendar(seminar_names['junior_strings'],
#             'https://www.google.com/calendar/ical/bkhromh605bm44dl8fuq4dip'
#             '58%40group.calendar.google.com/public/basic.ics'),
    Calendar(seminar_names['relativity'],
             'https://www.maths.ox.ac.uk/events/list/688/all/calendar.ics'),
    Calendar(seminar_names['all_of_physics'],
             'https://www2.physics.ox.ac.uk/ical/research/seminars/series/particles-and-fields-seminar'),
    Calendar(seminar_names['twistor'],
             'https://www.maths.ox.ac.uk/events/list/701/all/calendar.ics'),
)

# Calendar sources (seminar series) whose events should be included by
# default. All others must be picked manually using the
# http://strings-oxford.appspot.com/cal/admin view.
default_series = (
    seminar_names['strings'], 
    seminar_names['qft'], 
    seminar_names['math_colloquium'],
    seminar_names['junior_strings'],
    seminar_names['math_phys'],
    seminar_names['algebraic_symplectic'],
    seminar_names['relativity'],
    seminar_names['twistor'],
    seminar_names['geometry_analysis'],
    seminar_names['holography'],
    seminar_names['particle_pheno'],
    seminar_names['theoretical_physics'],
    seminar_names['particles_and_fields'],
    seminar_names['physics_colloquia'],
)

default_series_lower_case = tuple(s.lower() for s in default_series)


# How to start the abstract.
abstract_intro = 'Further information:'

# The following will be stripped off if they are at the beginning of
# the abstract (case insensitive)
strip_abstract_intro = tuple(s.lower() for s in [
    abstract_intro,
    'more information:',
    'furthern information:',
    'abstract:',
])
                             

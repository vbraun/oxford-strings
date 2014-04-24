# -*- coding: utf-8 -*-
"""
Main entry point
"""


import sys
import os

from webapp2 import WSGIApplication, Route, uri_for
from google.appengine.api import users

from app.base_view import PageRequestHandler
from app.editable_view import WikiPage, Editor, History
from app.cron import IcalSyncer
from app.calendar_view import (
    CalendarAdmin, Seminars, ThisWeek, BagLunch,
)

application = WSGIApplication([
    Route(r'/', WikiPage),
    Route(r'/<name:[^/]*\.html>', WikiPage, name='wiki-page'),
    Route(r'/edit/<name:[^/]*\.html>', Editor, name='editor'),
    Route(r'/history/<name:[^/]*\.html>', History, name='history'),
    Route(r'/cal/seminars.html', Seminars, name='seminars'),
    Route(r'/cal/this_week.html', ThisWeek, name='this-week'),
    Route(r'/cal/bag_lunch.html', BagLunch, name='bag-lunch'),
    Route(r'/cal/admin', CalendarAdmin, name='calendar-admin'),

    # Not implemented
    #    Route(r'/cal/edit', CalendarEdit, name='calendar-new'),
    #    Route(r'/cal/edit/<uid>', CalendarEdit, name='calendar-edit'),

    Route(r'/cal/sync', IcalSyncer, name='cron-sync'),
], debug=True)


# -*- coding: utf-8 -*-
"""
Configuration

All configuration goes into this file
"""

import os

# Set up paths. Only change this if you reorganize the project directory
APP_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(APP_DIR, 'templates')
CSS_DIR = os.path.join(APP_DIR, 'static', 'css')
JS_DIR = os.path.join(APP_DIR, 'static', 'js')
LIB_DIR = os.path.join(APP_DIR, 'lib')


from app.menu import MenuItem
menu_items = (
    MenuItem('Home',            'index.html'),
    MenuItem('Members',         'members.html'),
    MenuItem('Research',        'research.html'),
    MenuItem('Seminars',        'seminars.html'),
    MenuItem('Bag lunch',       'bag_lunch.html', 1),
    MenuItem('This week',       'thisweek.html', 1),
    MenuItem('Graduate study',  'graduates.html'),
)



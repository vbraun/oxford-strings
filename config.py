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

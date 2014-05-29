# -*- coding: utf-8 -*-
"""
Configuration for development (tests etc)
"""
    

import os

from google.appengine.api import lib_config
#from app.config import config as app_config
import app.config as app_config
from develop.sdk_path import get_sdk_path

class _ConfigDefaults(object):

    # Set up paths. Only change this if you reorganize the project directory
    HOME_DIR = app_config.HOME_DIR
    TEMPLATES_DIR = app_config.TEMPLATES_DIR
    CSS_DIR = app_config.CSS_DIR
    JS_DIR = app_config.JS_DIR

    # whether or not we are running on the dev appserver (True) or on Appengine (False)
    DEV_SERVER = False

    TEST_DIR = os.path.join(app_config.HOME_DIR, 'app', 'test')

    get_sdk_path = get_sdk_path


config = lib_config.register('develop',  _ConfigDefaults.__dict__)


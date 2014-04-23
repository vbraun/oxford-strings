# -*- coding: utf-8 -*-
"""
Configuration for when NOT running on Appengine.
"""

from app.config import *

# import os
# import sys


# HOME_DIR = os.path.dirname(os.path.dirname(__file__))

TEST_DIR = os.path.join(APP_DIR, 'app', 'test')


GIT_CONFIG_HELP = """
Google Appengine SDK path not configured. Run something like

    git config googleappengine.path /home/vbraun/opt/google_appengine

in the project directory to set it up.
""".strip()

def get_sdk_path():
    from .git_interface import GitInterface, GitError
    git = GitInterface()
    try:
        return git.config('googleappengine.path').strip()
    except GitError:
        print(GIT_CONFIG_HELP)
        import sys
        sys.exit(1)
    

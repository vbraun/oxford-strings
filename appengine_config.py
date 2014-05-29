import os
import sys

# whether or not we are running on the dev appserver (True) or on Appengine (False)
DEV_SERVER = os.environ.get('SERVER_SOFTWARE','').startswith('Development') or \
             'IPython' in sys.modules


develop_DEV_SERVER = DEV_SERVER

strings_oxford_DEV_SERVER = DEV_SERVER



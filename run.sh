#!/bin/sh

SDK="$HOME/opt/google_appengine"


exec "$SDK/dev_appserver.py" . \
  --host 127.0.0.1 \
  --port 8080 \
  --skip_sdk_update_check


# todo
#   --python_startup_script=autocompile_coffee.py \

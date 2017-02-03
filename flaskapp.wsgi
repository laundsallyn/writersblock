#!/usr/bin/env python

#activate_this = '/var/www/flaskapp/flaskapp/venv/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/flaskapp/")

from flaskapp import app as application
application.secret_key = 'dev_secret_key'


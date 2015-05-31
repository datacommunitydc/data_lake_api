#!/usr/bin/env python
### Apache WSGI config file

# Add apy to python load path and import api
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(1, '/home/ubuntu/datacommunitydc-api')

from api import app as application

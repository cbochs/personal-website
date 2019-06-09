#!/user/bin/python3
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/cbochs/website')

from FlaskApp import app as application

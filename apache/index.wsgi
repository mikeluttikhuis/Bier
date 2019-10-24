#! /usr/bin/python3.6

import logging
import sys
sys.path.insert(1, '/var/www/bier.mikeluttikhuis.nl/config')
import config

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/bier.mikeluttikhuis.nl')
from index import app as application
application.secret_key = config.secret_key

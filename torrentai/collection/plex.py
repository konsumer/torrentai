"""
Uses plex API to get info about current collection

env-vars:
  PLEX_HOST="localhost:32400" # the hostname of the plex server

"""

import os

PLEX_HOST=os.getenv('PLEX_HOST', 'localhost:32400')

class CollectionManager:
  pass
"""
Uses plex API to get info about current collection

env-vars:
  URL_PLEX="http://localhost:32400" # the hostname of the plex server

"""

import os
from torrentai import CollectionManagerBase

URL_PLEX=os.getenv('URL_PLEX', 'http://localhost:32400')

class CollectionManager(CollectionManagerBase):
  pass

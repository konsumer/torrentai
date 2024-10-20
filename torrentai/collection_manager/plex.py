"""
Uses plex API to get info about current collection

env-vars:
  URL_PLEX="http://localhost:32400" # the hostname of the plex server
  PLEX_CLAIM="claim_WHATEVER"
"""

import os
from torrentai import CollectionManagerBase

URL_PLEX=os.getenv('URL_PLEX', 'http://localhost:32400')
PLEX_CLAIM=os.getenv('URL_PLEX', 'claim_whatever')

class CollectionManager(CollectionManagerBase):
  pass

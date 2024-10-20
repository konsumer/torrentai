"""
This will collect media-info from plex.

env-vars:
  URL_PLEX="http://localhost:32400" # the hostname of the plex server
  PLEX_CLAIM="claim_WHATEVER"
"""

import os
from torrentai import MediaInfoBase

URL_PLEX=os.getenv('URL_PLEX', 'http://localhost:32400')
PLEX_CLAIM=os.getenv('URL_PLEX', 'claim_whatever')

class MediaInfo(MediaInfoBase):
  pass

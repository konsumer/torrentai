"""
This will collect media-info from plex.

env-vars:
  URL_PLEX="http://localhost:32400" # the hostname of the plex server

"""

import os
from torrentai import MediaInfoBase

URL_PLEX=os.getenv('URL_PLEX', 'http://localhost:32400')

class MediaInfo(MediaInfoBase):
  pass

"""
This will collect media-info from plex.

env-vars:
  PLEX_HOST="localhost:32400" # the hostname of the plex server

"""

import os
from torrentai import MediaInfoBase

PLEX_HOST=os.getenv('PLEX_HOST', 'localhost:32400')

class MediaInfo(MediaInfoBase):
  pass

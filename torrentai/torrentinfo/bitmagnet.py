"""
bitmagnet API for collecting lists of torrents, and allowing you to search

env-vars:
  BITMAGNET_HOST="localhost:3333" # the hostname of the bitmagnet server

"""

import os

BITMAGNET_HOST=os.getenv('BITMAGNET_HOST', 'localhost:3333')

class TorrentSource:
  pass
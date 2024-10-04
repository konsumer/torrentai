"""
bitmagnet API for collecting lists of torrents, and allowing you to search

env-vars:
  BITMAGNET_HOST="localhost:3333" # the hostname of the bitmagnet server

"""

import os
from torrentai import TorrentSourceBase

BITMAGNET_HOST=os.getenv('BITMAGNET_HOST', 'localhost:3333')

class TorrentSource(TorrentSourceBase):
  def __init__(self, host=BITMAGNET_HOST):
    self.host = host

  def get_torrents(self, type:str, title:str, year:str, artist:str):
    return [
      {
        "id": "5173t93EYdxeb",
        "title": "Movie 1",
        "seeders": 1,
        "leechers": 6,
        "size": "1G"
      },
      {
        "id": "2t6MVuh6sN8Co",
        "title": "Movie 2",
        "seeders": 10,
        "leechers": 30,
        "size": "1.4G"
      },
      {
        "id": "KZybiZPBeBogc",
        "title": "Movie 3",
        "seeders": 30,
        "leechers": 60,
        "size": "1.5G"
      },
    ]

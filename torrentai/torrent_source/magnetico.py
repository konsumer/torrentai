"""
magnetico sqlite interface for collecting lists of torrents, and allowing you to search

env-vars:
  MAGNETICO_FILE="./torrents.sqlite" # the filename with your torrent info

"""

import os
from torrentai import TorrentSourceBase

MAGNETICO_FILE=os.getenv('MAGNETICO_FILE', './torrents.sqlite')

class TorrentSource(TorrentSourceBase):
  def __init__(self, file=MAGNETICO_FILE):
    self.file = file

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

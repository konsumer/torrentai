"""
qtorrent API to download torrents

env-vars:
  QTORERNT_HOST="localhost:8080" # the hostname of the qtorrent web-ui server

"""

import os
from torrentai import TorrentManagerBase

QTORERNT_HOST=os.getenv('QTORERNT_HOST', 'localhost:8080')

class TorrentManager(TorrentManagerBase):
  def __init__(self):
    pass

  def download_torrent(self, id):
    pass

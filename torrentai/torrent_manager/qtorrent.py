"""
qtorrent API to download torrents

env-vars:
  URL_QTORRENT="http://localhost:8080" # the hostname of the qtorrent web-ui server

"""

import os
import qbittorrentapi
from torrentai import TorrentManagerBase
from urllib.parse import urlparse, quote

URL_QTORRENT=os.getenv('URL_QTORRENT', 'http://localhost:8080')

class TorrentManager(TorrentManagerBase):
  def __init__(self, url=URL_QTORRENT):
    u=urlparse(url)
    conn_info = {
        "host": u.hostname,
        "port": u.port,
        "username": u.username,
        "password": u.password,
    }
    self.qbt = qbittorrentapi.Client(**conn_info)

  def download_torrent(self, id, title):
    if self.qbt.torrents_add(urls=f"magnet:?xt=urn:btih:{id}&dn={quote(title)}") != "Ok.":
      raise Exception("Failed to add torrent.")

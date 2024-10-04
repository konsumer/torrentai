# plex API to get media-info
from torrentai.media_info.plex import MediaInfo

# ollama LLM server for queries
from torrentai.llm_query.ollama import LlmQuery

# bitmagnet API for collecting lists of torrents, and allowing you to search
from torrentai.torrent_source.bitmagnet import TorrentSource

# qtorrent API to download torrents
from torrentai.torrent_manager.qtorrent import TorrentManager

# plex API to get info about current collection
from torrentai.collection_manager.plex import CollectionManager

from torrentai import TorrentAI

server=TorrentAI(
  MediaInfo(),
  LlmQuery(),
  TorrentSource(),
  TorrentManager(),
  CollectionManager()
)

# setup UI

import chainlit as cl
cl.on_chat_start(server.on_chat_start)
cl.on_message(server.on_message)

# plex API to get media-info
from torrentai.mediainfo.plex import MediaInfo

# ollama LLM server for queries
from torrentai.llm.ollama import LlmQuery

# bitmagnet API for collecting lists of torrents, and allowing you to search
from torrentai.torrentinfo.bitmagnet import TorrentSource

# qtorrent API to download torrents
from torrentai.downloader.qtorrent import TorrentManager

# plex API to get info about current collection
from torrentai.collection.plex import CollectionManager

from torrentai import TorrentAI

server=TorrentAI(MediaInfo(), LlmQuery(), TorrentSource(), TorrentManager())

# setup UI

import chainlit as cl

@cl.on_chat_start
async def on_chat_start():
  await server.on_chat_start()

@cl.on_message
async def on_message(message: cl.Message):
  await server.on_message(message)

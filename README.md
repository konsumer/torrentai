This is an extensible engine for applying an LLM to collecting media. It will enable you to make a very simple request engine for plex (more media-managers to come) that is intelligent, will find media for you, and manage downloading it.

I designed this as a very simple prompt for my media-server, so people can ask for things they want, and get pretty simple responses that are aware of the current collection, finding torrents, downloaiding them, etc.


## usage

Some example queries:

```
Get the movie "Legend (1985)"
Get the movie "Labrynth"
Get the movie Goonies
Are there any good copies of album "The Fame" by Lady Gaga?
```

## setup

Configuration is done with code & env-vars. You will need a few stages to do stuff, and each stage is implemented in a few ways, for maximum flexibility. Here is an example entry-point that uses plex for gathering info/collection, qtorrent for downloading torrents and bitmagnet to find them:

```py
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
```

You can run this with:

```
chainlit run example.py --host 0.0.0.0 --port 5100
```

At the top of each of these adapter-files, you will see instructions for configuring it.


### docker

I have included a [docker-compose](docker-compose.yml) to get started quickly, which will spin up all of these services for you:

```
# get the code
git clone https://github.com/konsumer/torrentai.git
cd torrentai

# make sure to edit .env after this
cp .env.example .env

# run it
docker compose up -d
```

## ideas

- more adapters & example-combinations of services
- minimal configuration that doesn't need much else other than itself (use TMDB directly, inline LLM, do it's own DHT-scraping/torrent-downloading/etc.)
- handle more types of queries, maybe with multiple tool-passes

This project should be able to replace what sonarr/radarr/etc do, in terms of finding torrents & triggering downloads, and gets rid of a lot of overlap (each needs sources & torrent-client and tons of other things configured.) I'd like to implement many source/download adapters, so this project can be used similarly (use RSS feeds and other torrent-search things.)

This is an extensible engine for applying an LLM to collecting media. It will enable you to make a very simple request engine for plex (more media-managers to come) that is intelligent, will find media for you, and manage downloading it.

I designed this as a very simple prompt for my media-server, so people can ask for things they want, and get pretty simple responses that are aware of the current collection, finding torrents, downloaiding them, etc.


## setup

Configuration is done with code & env-vars. You will need a few stages to do stuff, and each stage is implemented in a few ways, for maximum flexibility. Here is an example entry-point that uses plex for gathering info/collection, qtorrent for downloading torrents and bitmagnet to find them:

```py
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
server.start()
```

You can run this with:

```
python3 example.py
```

At the top of each of these adapter-files, you will see instructions for installing & configuring it.


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

The eventual goal is to make more example-combinations of services, so you can use it however you want, but I built it for my setup (ollama/plex/bitmagnet/qtorrent) first.

With each of these services, I was already using them, and wanted their webui/etc to manage externally, but I'd like to also have a minimal configuration that doesn't need much else other than itself (use TMDB, inline LLM, do it's own DHT-scraping/torrent-downloading/etc.)

This project should be able to replace what sonarr/radarr/etc do, in terms of finding torrents & triggering downloads, and gets rid of a lot of overlap (each needs sources & torrent-client and other things configured.) I'd like to implement many source/download adapters, so this project can be used similarly (use rss feeds and other torrent-search things) but we have a slightly differnt goals.


"""
bitmagnet API for collecting lists of torrents, and allowing you to search

env-vars:
  URL_BITMAGNET="http://localhost:3333/graphql" # the hostname of the bitmagnet server

"""

import os
from torrentai import TorrentSourceBase
from python_graphql_client import GraphqlClient

URL_BITMAGNET=os.getenv('URL_BITMAGNET', 'http://localhost:3333/graphql')

GET_TORRENTS="""
query TorrentContentSearch($queryString: String, $contentType: ContentType) {
  torrentContent {
    search(query: {queryString: $queryString, limit: 30, cached: true, totalCount: true}, facets: { contentType: { aggregate: true, filter: [$contentType]}}, orderBy: [{field: Seeders, descending: true}]) {
      items {
        infoHash
        contentType
        seeders
        leechers
        videoResolution
        videoCodec
        title
        content {
          releaseYear
          popularity
          overview
          runtime
        }
        torrent { size }
      }
    }
  }
}
"""


class TorrentSource(TorrentSourceBase):
  def __init__(self, endpoint=URL_BITMAGNET):
    self.gql = GraphqlClient(endpoint=endpoint)

  def get_torrents(self, type:str, title:str, year:str, artist:str):
    variables = {
      "queryString": title,
      "contentType": type
    }

    if type == "album":
      variables['contentType']="music"

    if type == "tv":
      variables['contentType']="tv_show"

    if type == "album" and artist is not None:
      variables['queryString']=f"{artist} - {title}"

    if year is not None:
       variables['queryString']=f"{variables['queryString']} ({year})"

    r = self.gql.execute(query=GET_TORRENTS, variables=variables)
    print(r)
    out = []
    for result in r['data']['torrentContent']['search']['items']:
      o = {
        "id": result['infoHash'],
        "seeders": result['seeders'],
        "leechers": result['leechers'],
        "title": result['title'],
        "year": year,
        "runtime": 0,
        "overview": "",
        "size": result['torrent']['size']
      }
      # content is mostly for movies, and often not set
      if result['content'] is not None:
        o['year'] = result['content']['releaseYear']
        o['runtime'] = result['content']['runtime'],
        o['overview'] = result['content']['overview'],
      out.append(o)
    return out

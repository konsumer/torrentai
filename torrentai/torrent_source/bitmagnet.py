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
    search(query: {queryString: $queryString, limit: 10, cached: true, totalCount: true}, facets: { contentType: { aggregate: true, filter: [$contentType]}}, orderBy: [{field: Seeders, descending: true}]) {
      items {
        infoHash
        seeders
        leechers
        content {
          title
          externalLinks { url }
          releaseYear
          popularity
          overview
          runtime
          collections { name }
        }
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

    r = self.gql.execute(query=GET_TORRENTS, variables=variables)
    print(r)
    out = []
    for result in r['data']['torrentContent']['search']['items']:
      out.append({
        "id": result['infoHash'],
        "seeders": result['seeders'],
        "leechers": result['leechers'],
        "title": result['content']['title'],
        "year": result['content']['releaseYear'],
        "runtime": result['content']['runtime'],
        "overview": result['content']['overview'],
        "links": [i['url'] for i in result['content']['externalLinks']]
      })
    return out

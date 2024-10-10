## flows

These are some flows I need to implement.

> **USER**: Get the movie "Legend"

Here I mean [the 80s fantasy movie](https://www.themoviedb.org/movie/11976-legend?language=en-US)


Reasoning:

- detect they want movie, figure out what movie they mean. tmdb [returns 3,237 movies](https://www.themoviedb.org/search?language=en-US&query=legend) for "legend". Pick top-5 and ask user to choose, or "None of these" to get more in list. Maybe there could be some AI to pick best candidates, but I am not sure how to do this, in a logistical-sense. It might be possible to use the data that is already in database (to save trip to tmdb)
- User picks [11976](https://www.themoviedb.org/movie/11976-legend?language=en-US)
- Check plex for the movie. if it's already available, give user link.
- Use that id to lookup content & related torrents in db: `select * from content where id='11976';` I get 1 result, which means there are torrents for that movie. if there are none, tell the user.
- Get torrent info with `select torrent_contents.id, torrent_contents.video_resolution, torrent_contents.video_source, torrent_contents.video_codec, torrent_contents.published_at, torrent_contents.size, torrent_contents.seeders, torrent_contents.leechers from torrent_contents where torrent_contents.content_type='movie' and torrent_contents.content_id='11976' and torrent_contents.seeders != 0;`, use user-specified heuristics like "prefer most seeders/certain dimensions/quality/filesize/etc". if there are still multiple options, ask the user. if there are none, tell the user.
- user picks `81773fff9b75807735e243abda351f8f2cec6f32:movie:tmdb:11976` so build a magnet link.
- Check if qtorrent is already downloading this movie. Try to make it smart, like check magnet, but also titles of running torrents
- queue download and tell user
- allow user-questions for status like "how is my Legend download doing?"
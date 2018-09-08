# lastfm-playlist-generator

Create .m3u playlists with lastfm API.

## Interface with Last.fm API

LastfmClient object allows for interaction with Last.fm API.  
Will need to provide an API_KEY upon object creation.

## Create Different Types of Playlists

Playlist_Creator object allows for the creation of different types of playlists.  
Playlists are created by iterating through .mp3 files under a music_directory.  
Files are added to .m3u playlist file if they match criteria gathered from arguments and last.fm data.
#### create_playlists_for_similar_artists(client, artist)
Look up similar artists for each mp3 file.  
If specified artist artist is among these similar artists, add track to playlist.
#### create_playlists_for_tracktags(client)
Look up track tags for each mp3 file.  
Create playlist for each unique tag.
#### create_playlist_for_tag(client, playlist_name, pattern)
Look up track tags for each mp3 file.  
If track tag matches pattern, add to playlist.  
Use regular expression to specify pattern. (Eg. "[Hh]ip[- ]?[Hh]op")

## Getting Started

```
import lastfm
import playlist

# Sample key. Create your own at https://www.last.fm/api/account/create
API_KEY = 'c22db4d2289e16df56df67c33f12da9c'

client = lastfm.LastfmClient(API_KEY)

music_dir = '/home/fultonj/Music'  //Directory where music files are stored
playlist_dir = '/home/fultonj/Music/playlists'  //Directory to save playlists
myplaylist.Playlist_Creator(playlist_dir, music_dir)

# Create different types of playlists
myplaylist.create_playlist_for_similar_artists(client, 'artist_name')
myplaylist.create_playlist_for_tag(client, 'playlist_name', 'genre_pattern')
myplaylist.create_playlist_for_tracktags(client)
```

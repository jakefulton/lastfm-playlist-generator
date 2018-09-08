#! /usr/bin/python3

import lastfm
import os
import re
import collections
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3


class Playlist_Creator:
    def __init__(self, playlist_dir, music_dir):
        """
        Object allows for the creation of different types of playlists

        Playlist folder is where you want to keep the created playlists
        Music folder is the root directory for where your music is stored
        Playlist folder and music folder can be same directory
        """
        self._playlist_dir = playlist_dir
        self._music_dir = music_dir
        self._playlists = set()
        self._track_information = collections.namedtuple('track_information',
                'location artist title, length')

        self._check_existing_playlists()

    def _check_existing_playlists(self):
        """
        Keep track of existing playlists
        """
        for playlist in os.listdir(self._playlist_dir):
            if re.search('\.[Mm]3[Uu]$', playlist):
                self._playlists.add(playlist)

    def _get_track_information(self, root, file_name):
        """
        Get track information for mp3 file
        """
        track_location = os.path.join(root, file_name)
        track = EasyID3(track_location)
        track_artist = track['artist'][0]
        track_title = track['title'][0]
        track_length = int(MP3(track_location).info.length)
        return self._track_information(track_location, track_artist, track_title, track_length)

    def _add_to_playlist(self,playlist_name,track_length,track_artist,track_title,track_location):
        """
        Use track infromation to add track to playlist specified by playlist_name
        """
        full_playlist_name = "{}.m3u".format(playlist_name)
        playlist_path = os.path.join(self._playlist_dir, full_playlist_name)

        playlist = open(playlist_path, 'a')
        #Create header for new playlists
        if full_playlist_name not in self._playlists:
            playlist.write("#EXTM3U\n")
            self._playlists.add(full_playlist_name)

        #Add track to playlist
        playlist.write("#EXTINF:{}, {} - {}\n{}\n".format(
            track_length, track_artist, track_title, track_location))
        playlist.close()

    def create_playlist_for_similar_artists(self, client, artist):
        """
        Use lastfm to find artists similar to a user-specified artist
        Create a playlist for all mp3s under music folder with
            similar or the same artist as user-specified artist
        """
        #Keep track of existing playlists
        self._check_existing_playlists()
        if "{}.m3u".format(artist) in self._playlists:
            print("There is already a playlist for {}".format(playlist_name))
            return

        #Get similar artists for an artist
        Similar_artists = lastfm.Similar_artists()
        artist_list = Similar_artists.get_similar_artists(client, artist)
        for name in artist_list:
            print(name)
        if not artist_list:
            return

        #Iterate through mp3 files under music directory
        for (root, dirs, files) in os.walk(self._music_dir):
            for file_name in files:
                if re.search('\.[Mm][Pp]3$', file_name):

                    #Get track information
                    track_info = self._get_track_information(root, file_name)

                    #If artist for track is a similar artist, add to playlist
                    for similar_artist in artist_list:
                        pattern = ".*{}|{}.*".format(artist, track_info.artist)
                        if re.search(pattern, similar_artist):
                            self._add_to_playlist(artist, track_info.length,
                                    track_info.artist, track_info.title, track_info.location)
                            break

        #Check if new playlist was created
        if "{}.m3u".format(artist) not in self._playlists:
            print("Did not find any tracks with artists similar to {}".format(artist))

    def create_playlists_for_tracktags(self, client):
        """
        Look up track tags for each mp3 file under music folder
        Create playlist in playlist folder for each unique tag
        """
        #Keep track of existing playlists
        self._check_existing_playlists()

        #iterate through mp3 files under music directory
        for (root, dirs, files) in os.walk(self._music_dir):
            for file_name in files:
                if re.search('\.[Mm][Pp]3$', file_name):

                    #Get track information
                    track_info = self._get_track_information(root, file_name)

                    #Get tags for a track 
                    Track_tags = lastfm.Track_tags()
                    tags= Track_tags.get_tags_for_track(client, track_info.artist, track_info.title)
                    print("{} : {}".format(track_info.artist, track_info.title))
                    if not tags:
                        print("     No tags were found for {} by {}".format(
                            track_info.title, track_info.artist))
                    #Iterate through tags
                    for tag in tags:
                        print("     {}".format(tag))

                        #Create playlist for each unique tag
                        self._add_to_playlist(tag, track_info.length,
                                track_info.artist, track_info.title, track_info.location)

    def create_playlist_for_tag(self, client, playlist_name, pattern):
        """
        Look up track tags for each mp3 file under music folder
        If track tag matches user specified pattern, add to playlist
        Use regular expression to specify pattern
            Ex/ "[Hh]ip[- ]?[Hh]op"
        """
        #Keep track of existing playlists
        self._check_existing_playlists()
        if "{}.m3u".format(playlist_name) in self._playlists:
            print("There is already a playlist named {}".format(playlist_name))
            return

        #Iterate through mp3 files under music director
        for (root, dirs, files) in os.walk(self._music_dir):
            for file_name in files:
                if re.search('\.[Mm][Pp]3$', file_name):

                    #Get track information
                    track_info = self._get_track_information(root, file_name)

                    #Get tags for a track
                    Track_tags = lastfm.Track_tags()
                    tags = Track_tags.get_tags_for_track(client, track_info.artist, track_info.title)
                    #Iterate through tags
                    for tag in tags:

                        #Check if tag matches pattern
                        if re.search(pattern, tag):
                            self._add_to_playlist(playlist_name, track_info.length,
                                    track_info.artist, track_info.title, track_info.location)
                            break

        #Check if new playlist was created
        if "{}.m3u".format(artist) not in self._playlists:
            print("Did not find any tags for {}".format(pattern))

import requests
import json

base_url = 'http://ws.audioscrobbler.com/2.0'

class LastfmClient:
    def __init__(self, api_key):
        """
        Create a lastfm API client

        api_key must be obtained from lastfm
        """

        self._key = api_key
        self._track_tags = {}

    def client_work(self, request_url, request_params):
        """
        Passes a request url and paramaters to lastfm and returns the response
        """
        request_params['api_key'] = self._key
        try:
            response = requests.get(
                    url = request_url,
                    params = request_params)
            return json.loads(response.text)
        except requests.exceptions.ReqeustException:
            print('HTTP Request Failed')
            return None

class Track_tags:
    def __init__(self):
        self._url = "{}?method=track.gettoptags".format(base_url)
    def get_tags_for_track(self, client, artist, track, autocorrect=1):
        """
        Must pass in a LastfmClient as an argument
        Interacts with lastfm to return a list of tags for a song
        """
        params = {'artist' : artist, 'track' : track, 'autocorrect': autocorrect, 'format' : 'json'}
        parsed_json = client.client_work(self._url, params)
        tags = []
        try:
            for tag in parsed_json['toptags']['tag']:
                tags.append(tag['name'])
            return tags
        except KeyError:
            print("{} by {} : {}".format(track, artist, parsed_json['message']))
            return tags

class Similar_artists:
    def __init__(self):
        self._url = "{}?method=artist.getsimilar".format(base_url)
    def get_similar_artists(self, client, artist, autocorrect=1):
        """
        Must pass in a LastfmClient as an argument
        Interacts with lastfm to return a list of similar artists for an artist
        """
        params = {'artist' : artist, 'autocorrect' : autocorrect, 'format' : 'json'}
        parsed_json = client.client_work(self._url, params)
        similar_artists = []
        try:
            for artist in parsed_json['similarartists']['artist']:
                similar_artists.append(artist['name'])
            return similar_artists
        except KeyError:
            print(parsed_json['message'])
            return similar_artists

#!/bin/python

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import datetime
from pathlib import Path

import json
import sys

class Track:
    name = None
    album = None
    artists = None

    def __init__(self, track):
        self.name = track['name']
        self.album = Album(track['album']).__dict__
        self.artists = list(map(lambda artist: artist['name'], track['artists']))

class Album:
    name = None
    release_date = None

    def __init__(self, album):
        self.name = album['name']
        self.release_date = album['release_date']

def playlistsOfUser(username):
    playlists = sp.user_playlists(user)

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            playlistTracks = getTracksFrom(playlist)
            directory = f'{username}/{playlist["name"]}'
            Path(directory).mkdir(parents=True, exist_ok=True)
            f = open(f'{directory}/{now.isoformat()}.json', "w")
            f.write(json.dumps(playlistTracks))
            f.close()

        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None


def getTracksFrom(playlist):
    offset = 0

    playlistTracks = []
    while True:
        response = sp.playlist_items(playlist['id'], offset=offset)

        if (response is None) or len(response['items']) == 0:
            return playlistTracks

        offset = offset + len(response['items'])

        for i, item in enumerate(response['items']):
            playlistTracks.append(Track(item['track']).__dict__)


now = datetime.date.today()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

for i, user in enumerate(sys.argv[1:]):
    playlistsOfUser(user)

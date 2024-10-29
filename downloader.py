#!/bin/python

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import xspf_lib as xspf
import datetime
from pathlib import Path

def playlistsOfUser(username):
    now = datetime.date.today()
    directory = f'{username}/{now.year}/{now.month}/{now.day}'
    Path(directory).mkdir(parents=True, exist_ok=True)
    playlists = sp.user_playlists(user)
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            result = getXSFPlaylistFromPlaylist(playlist)

            f = open(f'{directory}/{playlist["name"]}.xsfp', "w")
            f.write(result.xml_string())
            f.close()
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None


def getXSFPlaylistFromPlaylist(playlist):
    xsfptracks = []
    playlistTracks = sp.playlist_tracks(playlist['id'])
    while playlistTracks:
        for i, playlistTrack in enumerate(playlistTracks['items']):
            if (playlistTrack['track'] is None) :
                continue
            xsfptracks.append(getInfoFromPlaylistTrack(playlistTrack))
        if playlistTracks['next']:
            playlistTracks = sp.next(playlistTracks)
        else:
            playlistTracks = None

    return xspf.Playlist(title=playlist['name'],
                             creator=playlist['owner']['display_name'],
                             annotation=playlist['description'],
                             location=playlist['external_urls']['spotify'],
                             identifier=playlist['uri'],
                             image=[playlist['images'][0]['url'] if len(playlist['images']) else None][0],
                             trackList=xsfptracks)


def getInfoFromPlaylistTrack(playlistTrack):
    track = playlistTrack['track']

    return xspf.Track(location=f'file://../artists/' +
                                    f'{track["artists"][0]["name"]}/' +
                                    f'{track["album"]["name"]}' +
                                    f'{[" (" + track["album"]["release_date"][:4] + ")" if track["album"]["release_date"] else ""]}/' +
                                    f'{track["name"]}.flac',
                              title=track['name'],
                              creator=','.join([artist['name'] for artist in track['artists']]),
                              album=track['album']['name'],
                              trackNum=[track['track_number'] if track['track_number'] else None][0],
                              duration=track['duration_ms'],
                              image=[track['album']['images'][0]['url'] if len(track['album']['images']) else None][0])

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
user = 'aboxofwine'

playlistsOfUser(user)

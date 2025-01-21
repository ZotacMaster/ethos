
from ethos.tools import helper

helper = helper.Format

r = helper.resolve_recents("../userfiles/recents.json")

playlist_path = '../userfiles/playlists'
playlists = helper.resolve_playlists(playlist_path)

tracks =[]
for playlist in playlists:
    tracks.append(helper.fetch_tracks_from_playlist(f"{playlist_path}/{playlist}"))

#print(tracks)

import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from yt_dlp import YoutubeDL

def get_spotify_client():
    client_id = "e904c35efb014b76bd8999a211e9b1e1"
    client_secret = "af18ccf7adae4ea7b37ca635c4225928"
    return Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

def get_song_metadata(query):  # Took 10 sec approx
    """
    Downloads the title of the requested song using yt-dlp, and uses Spotipy to get the song name in "song - artist" format.

    :param query: A string representing the search query used to find the audio content.
    :type query: str

    :return: A string in the format "song - artist name".
    :rtype: str
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1',
    }

    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(query, download=False)
        if 'entries' in result:
            result = result['entries'][0]
        title = result['title']

    spotify = get_spotify_client()
    search_result = spotify.search(q=title, type='track', limit=1)
    if search_result['tracks']['items']:
        track = search_result['tracks']['items'][0]
        song = track['name']
        artist = track['artists'][0]['name']
        metadata = f"{song} - {artist}"
    else:
        metadata = "Unknown - Unknown"

    return metadata

print(get_song_metadata("after hours"))

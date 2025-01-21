from yt_dlp import YoutubeDL
import os
from shazamio import Shazam
import base64
from dotenv import load_dotenv
from time import time
import asyncio
import httpx

load_dotenv()

# from spotipy import Spotify
# from spotipy.oauth2 import SpotifyClientCredentials

def get_audio_url(query):
    """
    Fetches the audio URL for a given search query using YoutubeDL. The function
    utilizes specific configuration options to return the best available audio
    source while ensuring no playlists are processed and only the top search
    result is fetched. It does not download the file, only extracts the URL for
    the audio stream.

    :param query: A string representing the search query used to find the audio
        content on YouTube. It can include keywords or phrases to search for.
    :type query: str

    :return: The URL string of the best audio stream available based on the given
        search query.
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
        return result['url']
"""
def get_spotify_client():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    return Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

async def get_song_metadata(query):  # Took 10 sec approx
    
    Downloads the title of the requested song using yt-dlp, and uses Spotipy to get the song name in "song - artist" format.

    :param query: A string representing the search query used to find the audio content.
    :type query: str

    :return: A string in the format "song - artist name".
    :rtype: str
    
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
"""

async def get_song_metadata(query): # Took 12 sec approx in async environment
    """
    Downloads a short audio snippet using yt-dlp, uses Shazam to recognize the song,
    and deletes the snippet once the metadata is retrieved.

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
        'outtmpl': 'snippet.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'postprocessor_args': [
            '-t', '5',  # Download only the first 5 seconds
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(query, download=True)
        if 'entries' in result:
            result = result['entries'][0]
        snippet_path = 'snippet.mp3'

    shazam = Shazam()
    out = await shazam.recognize_song(snippet_path)

    if out['matches']:
        song = out['track']['title']
        artist = out['track']['subtitle']
        metadata = f"{song} - {artist}"
    else:
        metadata = "Unknown - Unknown"

    os.remove(snippet_path)
    return metadata


# Normally took 4 sec for a online playback and 2 sec for a local playback.
#print(get_song_metadata("after hours"))



CLIENT_ID =  os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


async def get_spotify_token(client_id, client_secret):
    """
    Fetches authorization token from spotify
    
    Args: client_id(str), client_secret(str)
    
    return: spotify authorization token
    """

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    data = {"grant_type": "client_credentials"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
        response_data = response.json()

    if response.status_code != 200:
        raise Exception(f"Failed to get token: {response_data}")
    
    return response_data["access_token"]


async def search_tracks_from_spotify(track_name, token):
    """
    Searches for a track in spotify and returns first 10 entries of search results
    
    Args: track_name(str), token(str)
    
    return: tracks(list)
    """

    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "q": track_name,
        "type": "track",
        "limit": 10  
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response_data = response.json()

    if response.status_code != 200:
        raise Exception(f"Failed to fetch tracks: {response_data}")
    
    return response_data["tracks"]["items"]


async def fetch_tracks_list(track_name: str) -> list:
    """
    Returns a list of track name and artist name from tracks info

    Args: track_name(str)

    return: list
    """

    fetched_tracks = []
    try:
        
        start_time = time()
        token = await get_spotify_token(CLIENT_ID, CLIENT_SECRET)

        
        tracks = await search_tracks_from_spotify(track_name, token)
        

        if tracks:
            print(f"\nTracks found for '{track_name}':")
            for idx, track in enumerate(tracks, start=1):
                track_info = f"{idx}. {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}"
                #print(track_info)
                fetched_tracks.append(track_info)
        else:
            print(f"No tracks found for '{track_name}'.")
    
    except Exception as e:
        print(f"Error: {e}")

    finally:
        end_time = time()
        print("Time taken to get metadata = %.2f" % (end_time - start_time))
        #print(fetched_tracks)
        return fetched_tracks
    

#asyncio.run(fetch_tracks_list())


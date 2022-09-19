import scrapy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from decouple import config
import json

cid = config('SPOTIFY_CLIENT_ID')
secret = config('SPOTIFY_CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
spotipy = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

uri = 'spotify:artist:0L8ExT028jH3ddEcZwqJJ5'

discography = {
    'artist': spotipy.artist(uri)['name'],
    'albums': []
}

results = spotipy.artist_albums(uri, album_type='album')
albums = []
for album in results['items']:

    # if deluxe or remastered edition, skip 
    if 'deluxe' in album['name'].lower() or 'remastered' in album['name'].lower():
        continue
        
    discography['albums'].append({
        'name': album['name'],
        'year': album['release_date'][:4],
        'uri': album['uri'],
        'tracks': []
    })

for album in discography['albums']:
    album_tracks = spotipy.album_tracks(album['uri'])

    for track in album_tracks['items']:
        track_name = track['name']

        if 'version' in track_name.lower() or 'live' in track_name.lower():
            continue

        album['tracks'].append({
            'name': track_name,
            'uri': track['uri']
        })

    
with open('discography.json', 'w') as f:
    json.dump(discography, f)
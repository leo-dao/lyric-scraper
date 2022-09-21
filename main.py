import scrapy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from decouple import config
import json
from scrapy.crawler import CrawlerProcess
from lyric_scraper.spiders.lyric_spider import LyricSpider

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
        'num_tracks': 0,
        'tracks': []
    })

for album in discography['albums']:
    album_tracks = spotipy.album_tracks(album['uri'])

    for track in album_tracks['items']:
        track_name = track['name']

        if 'version' in track_name.lower() or 'live' in track_name.lower():
            continue
        
        # Removing - remastered, - live, etc.
        if ' - ' in track_name:
            track_name = track_name.split(' - ')[0]

        album['num_tracks'] += 1

        album['tracks'].append({
            'name': track_name,
            'uri': track['uri']
        })

#with open('discography.json', 'w') as f:
    #json.dump(discography, f)

process = CrawlerProcess()

for album in discography['albums']:
    for track in album['tracks']:
        process.crawl(LyricSpider, artist=discography['artist'], album=album['name'], song=track['name'])

process.start()

with open('error.json', 'w') as f:
    json.dump(LyricSpider.error, f)
    f.close()

with open('instances.json', 'w') as f:
    json.dump(LyricSpider.instance, f)
    f.close()
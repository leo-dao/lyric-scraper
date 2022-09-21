import scrapy
import json

class LyricSpider(scrapy.Spider):
    name = 'lyrics'

    instance = []

    error = []

    def count_lyric_instances(self, lyric, song):
        count = 0
        for section in song['contents']:
            for line in section['lyrics']:
                if lyric in line.lower():
                    count += 1
        return count

    def write_lyrics_to_file(self, song):
        with open('lyrics.json', 'a') as f:
            # If file is empty, writing the first line without a comma
            if f.tell() == 0:
                json.dump(song, f)
            else:
                f.write(',')
                json.dump(song, f)
            
            f.close()
        return

    def start_requests(self):
        artist = self.artist.replace(' ', '-').lower()
        song = self.song.replace(' ', '-').lower()

        song = ''.join(e for e in song if e.isalnum() or e == '-')

        url = f'https://genius.com/{artist}-{song}-lyrics'

        yield scrapy.Request(url=url, callback=self.parse, errback=self.errback)

    def parse(self, response):

        if response.status == 404:
            print(self.song, 'by', self.artsit, 'was not found')
            return

        song = {
            'artist': self.artist,
            'song': self.song,
            'contents': []
            }

        # array of lines in the song, including section headers
        lyrics_container = response.xpath("//div[@data-lyrics-container='true']//text()").extract()

        for line in lyrics_container:
            if line[0] == '[':
                
                song['contents'].append({
                    'section': line[1:-1],
                    'lyrics': []
                })

                # Moving to the lyrics of the section
                for lyric in lyrics_container[lyrics_container.index(line)+1:]:
                    
                    # Breaking the loop when the next section is found
                    if lyric[0] == '[':
                        break
                    else:
                        song['contents'][-1]['lyrics'].append(lyric)

        lyric_to_check = 'california'
        lyric_instance = self.count_lyric_instances(lyric_to_check, song)

        self.instance.append({
                'artist': self.artist,
                'album': self.album,
                'song': self.song,
                'instances': lyric_instance
            })

    def errback(self, failure):

        self.error.append({
            'artist': self.artist,
            'album': self.album,
            'song': self.song,
            'failed_url': failure.request.url,
            'error': failure.value.response.status
        })

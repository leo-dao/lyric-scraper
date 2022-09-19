import scrapy

class LyricSpider(scrapy.Spider):
    name = 'lyrics'

    def start_requests(self):
        artist = self.artist.replace(' ', '-').lower()
        song = self.song.replace(' ', '-').lower()
        url = f'https://genius.com/{artist}-{song}-lyrics'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        if response.status == 404:
            print(self.artist, self.song, 'ERROR NOT FOUND 404')
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

        print(song)


import scrapy

class LyricSpider(scrapy.Spider):
    name = 'lyrics'
    
    start_urls = ['https://genius.com/Soundgarden-black-hole-sun-lyrics']

    def parse(self, response):

        lyrics_container = response.xpath("//div[@data-lyrics-container='true']//text()").extract()

        sections = []

        for section in lyrics_container:
            if section[0] == '[':
                
                dic = {
                    'section': section[1:-1],
                    'lyrics': []
                }

                # Moving to the lyrics of the section
                for lyric in lyrics_container[lyrics_container.index(section)+1:]:
                    
                    # Breaking the loop when the next section is found
                    if lyric[0] == '[':
                        break
                    else:
                        dic['lyrics'].append(lyric)

                sections.append(dic)


        for section in sections:
            print(section['section'])
            print(section['lyrics'])
            print()


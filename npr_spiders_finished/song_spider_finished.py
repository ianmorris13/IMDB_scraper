# This worksheet was originally designed by [Erin George]
# (https://www.math.ucla.edu/~egeo/classes/spr21_pic16b-1/)
# (Department of Mathematics, UCLA), with subsequent
# revisions by John Zhang (Department of Mathematics, UCLA).

import scrapy

class SongSpider(scrapy.Spider):
    name = "song"
    start_urls = [
        'https://www.npr.org/sections/allsongs/606254804/new-music-friday'
    ]

    def parse(self, response):
        for tag in response.css('article h2.title a'):
            yield response.follow(tag, self.parse_article)

    def parse_article(self, response):
        artists = response.css('div.storytext li::text').re('(.+) —')
        albums = response.css('div.storytext li em::text').getall()
        songs = response.css('div.storytext li::text').re('Featured Song: "(.+)"')
        yield {
            'artists': artists,
            'albums': albums,
            'songs': songs
        }

# This worksheet was originally designed by [Erin George]
# (https://www.math.ucla.edu/~egeo/classes/spr21_pic16b-1/)
# (Department of Mathematics, UCLA), with subsequent
# revisions by John Zhang (Department of Mathematics, UCLA).

import scrapy

class ArchiveSpider(scrapy.Spider):
    name = "archive"
    start_urls = [
        f'https://www.npr.org/sections/news/archive?start={15*i+1}' for i in range(3)
    ]

    def parse(self, response):
        for article in response.css('article.item'):
            yield {
                'title': article.css('h2.title a::text').get(),
                'url': article.css('h2.title a::attr(href)').get(),
                'date': article.css('p.teaser time::attr(datetime)').get(),
                'teaser': article.css('p.teaser a::text').get()
            }

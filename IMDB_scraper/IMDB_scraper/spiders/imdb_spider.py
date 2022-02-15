import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = [
        'https://www.imdb.com/title/tt8714904/'
    ]

    def parse(self, response):#filmo-head-actor. head a
        
        topCst = response.css("div.ipc-title__wrapper a").attrib["href"] 

        if topCst:
            topCst = response.urljoin(topCst)

            yield scrapy.Request(topCst, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        
        actLst = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        for actor in actLst:
            actrPg = response.urljoin(actor)
            yield scrapy.Request(actrPg, callback = self.parse_actor_page) 

    def parse_actor_page(self, response):

        actNam = response.css('title::text').get()[0:-7]
        
        filmID = response.css("::attr(id)").re('filmography')
        tvName = response.css("a::text").getall()

        albums = response.css('div.storytext li em::text').getall()
        songs = response.css('div.storytext li::text').re('Featured Song: "(.+)"')
        yield {"actor" : actNam, "movie_or_TV_name" : movie_or_TV_name}



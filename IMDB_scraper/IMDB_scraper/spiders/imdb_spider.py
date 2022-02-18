import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = [
        'https://www.imdb.com/title/tt8714904/'
    ]

    def parse(self, response):
        '''
        Redirect scraper to webpage of full cast and crew of desired TV show 
        (under assumption you start on the TV Show's main IMDB page)

        @param self
        @param response: represents the website
        @yield: redirection to full cast and crew site
        '''
        
        #find where there is a hyperlink on the subgroup titled "Top Cast"
        topCst = response.css("div.ipc-title__wrapper a").attrib["href"] 

        #if it exists, take that link embedded in the hyperlink and
        #redirect scraper there
        if topCst:
            topCst = response.urljoin(topCst)

            yield scrapy.Request(topCst, callback = self.parse_full_credits)

    def parse_full_credits(self, response):
        '''
        Redirect sraper to actor's main webpage of each actor selected

        @param self
        @param response: represents the website
        @yield: redirection to actor main webpage
        '''

        #put actor name/ hyperlink in a list for all actors in the full cast and crew
        actLst = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        #redirect to the actor page for each actor in the list
        for actor in actLst:
            actrPg = response.urljoin(actor)
            yield scrapy.Request(actrPg, callback = self.parse_actor_page) 

    def parse_actor_page(self, response):
        '''
        Add to dictionary of every actor and every work they have acted in 

        @param self
        @param response: represents the website        
        @yield: adds dictionary  names and the works they have appeared in
        '''

        #grab the actors name
        actNam = response.css('title::text').get()[0:-7]
        
        #list of every work they have been apart of (producing, acting, etc...)
        flmLst = response.xpath("//*[@class='filmo-category-section']/div/b/a/text()").extract()
        
        #take the number of acting credits they have from 'Acting' tab
        #try with 'actor' tag, if that doesn't work, try with 'actress'
        #this depends on the individuals webpage
        try:
            actNum = int(response.xpath("//*[@id='filmo-head-actor']/text()").extract()[-1][2:-10])
        except:
            actNum = int(response.xpath("//*[@id='filmo-head-actress']/text()").extract()[-1][2:-10])

        #takes only the first actNum of works they been in, because this is their acting works
        actLst = flmLst[:actNum]

        #yeild dictionary of the actors and a list of all their works
        yield {"actor" : actNam, "movie_or_TV_name" : actLst}        



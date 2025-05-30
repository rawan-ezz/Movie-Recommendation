#what data i want?

import scrapy

class Inform(scrapy.Item):
    imdb_id = scrapy.Field()
    title = scrapy.Field()
    country = scrapy.Field()



 
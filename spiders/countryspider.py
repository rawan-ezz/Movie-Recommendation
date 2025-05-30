import scrapy
import json
from imdbscraper.items import Inform
#extracting country of each movie 
class Top250Spider(scrapy.Spider):
    name = "country_spider"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://m.imdb.com/chart/top/"]
 
    def parse(self, response):
        raw_data = response.css("script[id='__NEXT_DATA__']::text").get()
        json_data = json.loads(raw_data)
        needed_data = json_data['props']['pageProps']['pageData']['chartTitles']['edges']

        for movie in needed_data:
            node = movie['node']
            imdb_id = node['id']
            title = node['titleText']['text'] 

            # Create item and pass it to next request - using inform from Items.py
            item = Inform()
            item['title'] = title
            item['imdb_id'] = imdb_id

            url = f"https://www.imdb.com/title/{imdb_id}/"
            yield scrapy.Request(url=url, callback=self.parse_country, meta={'item': item})

    def parse_country(self, response):
        item = response.meta['item']
        item['country'] = response.xpath("//li[span[contains(text(),'Country of origin')]]//a/text()").get(default="Unknown")
        yield item

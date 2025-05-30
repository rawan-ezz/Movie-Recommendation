import scrapy
import json
# saved in final_one_result.json
class ImdbTop250Spider(scrapy.Spider):
    name = "imdb_top_250" #name of spider _ called by it when running the spider
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/"]

    def parse(self, response):
        # Extract __NEXT_DATA__ script
        json_data = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get() 
        # Load the script data as JSON
        data = json.loads(json_data)
        # Path to movies data in the JSON structure
        try:
            movies = data['props']['pageProps']['pageData']['chartTitles']['edges']
        except KeyError:
            self.logger.error("Couldn't find the expected data structure in the JSON.")
            return 

        # Loop through each movie and extract the required fields
        for movie in movies:
            node = movie['node']
            # Movie data extraction
            movie_id = node.get("id")
            title = node.get("titleText", {}).get("text")
            rank = movie.get("currentRank")
            release_year = node.get("releaseYear", {}).get("year")
            runtime = node.get("runtime", {}).get("seconds", 0)   
            rating = node.get("ratingsSummary", {}).get("aggregateRating")
            vote_count = node.get("ratingsSummary", {}).get("voteCount")
            description = node.get("plot", {}).get("plotText", {}).get("plainText")
            genres = [g['genre']['text'] for g in node.get("titleGenres", {}).get("genres", [])]
            poster_url = node['primaryImage']['url']
            #return
            yield {
                "id": movie_id,
                "title": title,
                "rank": rank,
                "release_year": release_year,
                "runtime_minutes": runtime,
                "rating": rating,
                "vote_count": vote_count,
                "description": description,
                "genres": genres,
                "poster_url": poster_url
            }

    
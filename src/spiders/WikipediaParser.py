from scrapy import Spider
from scrapy.http import Request, Response
from items import MoviesItem
import dateparser


class WikipediaSpider(Spider):
    name = 'wiki'

    list_page_url = 'https://en.wikipedia.org/wiki/Lists_of_films'

    prefix_url = 'https://en.wikipedia.org'

    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'ITEM_PIPELINES': {
            'pipelines.MoviesPipeline': 600
        },
        'DOWNLOAD_DELAY': 0.5,
    }

    def start_requests(self):
        yield Request(url=self.list_page_url, callback=self.parse_letters)

    def parse_letters(self, response: Response):
        for link in response.css('.wikitable td a::attr(href)').extract():
            yield Request(url=self.prefix_url + link, callback=self.parse_letter)

    def parse_letter(self, response: Response):
        for link in response.css('.columns li a::attr(href)').extract():
            yield Request(url=self.prefix_url + link, callback=self.parse)

    def parse(self, response: Response):
        item = MoviesItem()
        item.update({
            'name': response.css('#firstHeading i::text').extract_first(),
            'poster_url': response.css('.infobox img::attr(src)').extract_first(),
            'url': response.url
        })

        for tr in response.css('.infobox tr'):
            if tr.css('th::text').extract_first() == 'Country':
                item.update({
                    'country': tr.css('td::text').extract_first()
                })
            if tr.css('th div::text').extract_first() == 'Running time':
                item.update({
                    'running_time': tr.css('td::text').extract_first()
                })
            if tr.css('th div::text').extract_first() == 'Release date':
                release_date = tr.css('td li::text').extract_first()
                if release_date is not None:
                    item.update({
                        'release_year': dateparser.parse(release_date).year
                    })

        yield item

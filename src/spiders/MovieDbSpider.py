from scrapy import Spider
from scrapy.http import Request, Response
from items import MoviesItem
import dateparser


class MovieDbSpider(Spider):
    name = 'movie-db'

    start_url = 'https://www.themoviedb.org/movie?page={page}'

    site = 'themoviedb'

    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'ITEM_PIPELINES': {
            'pipelines.MoviesPipeline': 600
        },
        'DOWNLOAD_DELAY': 0.5,
    }

    def __init__(self, total_page=100, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_page = int(total_page)

    def start_requests(self):
        for page in range(self.total_page):
            yield Request(url=self.start_url.format(page=page + 1), callback=self.parse)

    def parse(self, response: Response):
        for film in response.xpath('//div[contains(@class,"results")]/div[contains(@class,"item")]'):
            item = MoviesItem()
            item.update({
                'name': film.xpath('./div[@class="info"]//a[contains(@class,"title")]/text()').extract_first(),
                'poster_url': film.xpath('./div[@class="image_content"]//img[contains(@class,"poster")]/@data-src').extract_first(),
                'url': 'https://www.themoviedb.org' + film.xpath('./div[@class="info"]//a[contains(@class,"title")]/@href').extract_first()
            })

            release_date = film.xpath('./div[@class="info"]//div[@class="flex"]/span/text()').extract_first()
            if release_date is not None:
                item.update({
                    'release_year': dateparser.parse(release_date).year
                })

            yield item

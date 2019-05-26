from scrapy import Spider
from scrapy.http import Request, Response
from items import MoviesItem
import re


class ListChallengesSpider(Spider):
    name = 'list-challenges'

    start_url = 'https://www.listchallenges.com/lists/movies/new'

    base_url = 'https://www.listchallenges.com'

    site = 'listchallenges'

    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'ITEM_PIPELINES': {
            'pipelines.MoviesPipeline': 600
        },
        'DOWNLOAD_DELAY': 0.5,
    }

    def start_requests(self):
        yield Request(url=self.start_url, callback=self.parse_lists)

    def parse_lists(self, response: Response):
        for href in response.xpath('//*[@id="MainContent_listRepeater_repeater"]//a[contains(@class,"card")]/@href').extract():
            yield Request(url=self.base_url + href, callback=self.parse)

        next_page = response.xpath('//a[contains(@class,"pageButtons-next")]/@href').extract_first()
        if next_page:
            yield Request(url=self.base_url + next_page, callback=self.parse_lists)

    def parse(self, response: Response):
        for film in response.xpath('//*[@id="repeaterListItems"]/div[contains(@class,"list-item")]'):
            item = MoviesItem()
            name = film.xpath('.//*[@class="item-name"]/text()').extract_first()
            if name:
                name = str(name).strip()
                result = re.search(r'.* (\(\d{4}\))$', name)
                if result:
                    item.update({'release_year': result.group(1).strip('()')})
                    name = name[:-6].strip()

                item.update({
                    'name': name,
                    'poster_url': film.xpath('.//*[@class="item-image-wrapper"]/img/@src').extract_first(),
                    'url': film.xpath('./@data-item-id').extract_first()
                })

                yield item

        next_page = response.xpath('//*[contains(@class,"pageButtons-next")]').extract_first()
        if next_page:
            url = None
            if '/list/' in response.url:
                result = re.search(r'(.*?)/list/(\d+)', response.url)
                if result:
                    page = int(result.group(2)) + 1
                    url = result.group(1) + '/list/' + str(page)

            if url is None:
                url = response.url + '/list/2'

            yield Request(url=url, callback=self.parse)

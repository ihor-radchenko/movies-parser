# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviesItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    unique_id = scrapy.Field()
    url = scrapy.Field()
    poster_url = scrapy.Field()
    country = scrapy.Field()
    running_time = scrapy.Field()
    release_year = scrapy.Field()

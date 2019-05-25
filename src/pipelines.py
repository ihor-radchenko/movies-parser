# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from connection import session
from models import Movie


class MoviesPipeline(object):
    def __init__(self):
        self.session = session

    def process_item(self, item, spider):
        if item.get('name') and not self.session.query(Movie).filter(Movie.url == item.get('url')).first():
            self.session.add(Movie(**item))
            self.session.commit()
            print('*' * 80)
            print('FILM PARSED: ' + item.get('name'))
            print('*' * 80)


# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from connection import session
from models import Movie
import hashlib


class MoviesPipeline(object):
    def __init__(self):
        self.session = session
        self.md5 = hashlib.md5()

    def process_item(self, item, spider):
        name = item.get('name')
        print(item)
        if name:
            url = item.get('url')
            self.md5.update(url.encode('utf-8'))
            item.update({
                'unique_id': self.md5.hexdigest()
            })
            exists = self.session.query(Movie).filter(Movie.unique_id == item.get('unique_id')).first()
            if not exists:
                movie = Movie(**item)
                self.session.add(movie)
                self.session.commit()


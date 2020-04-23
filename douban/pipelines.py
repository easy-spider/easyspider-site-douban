# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# TODO design the data format


import pymongo


class DoubanMoviePipeline(object):
    def __init__(self, mongo_url, mongo_db, mongo_col):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.mongo_col = mongo_col
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db=crawler.settings.get('BOT_NAME')+'_'+crawler.settings.get('SPIDER_NAME'),
            mongo_col=crawler.settings.get('TASK_ID')+'_'+crawler.settings.get('JOB_ID'),
        )

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        data = dict(item)
        self.db[self.mongo_col].insert(data)
        return item

    def close_spider(self, item):
        self.client.close()

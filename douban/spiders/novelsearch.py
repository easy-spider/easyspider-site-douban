# -*- coding: utf-8 -*-
import scrapy


# TODO finish novelsearch spider


class NovelsearchSpider(scrapy.Spider):
    name = 'novelsearch'
    allowed_domains = ['https://book.douban.com/']
    start_urls = ['http://https://book.douban.com//']

    def parse(self, response):
        pass

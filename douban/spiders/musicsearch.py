# -*- coding: utf-8 -*-
import scrapy


# TODO finish musicsearch spider


class MusicsearchSpider(scrapy.Spider):
    name = 'musicsearch'
    allowed_domains = ['https://music.douban.com/']
    start_urls = ['http://https://music.douban.com//']

    def parse(self, response):
        pass

# -*- coding: utf-8 -*-
import scrapy


# TODO finsh DouBan Search crawl
class MoviesearchSpider(scrapy.Spider):
    name = 'movieSearch'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    def parse(self, response):
        pass

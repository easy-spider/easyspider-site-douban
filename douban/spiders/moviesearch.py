# -*- coding: utf-8 -*-
import scrapy


# TODO finsh DouBan Search crawl
class MoviesearchSpider(scrapy.Spider):
    name = 'moviesearch'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']

    def __init__(self, **kwargs):
        self.key_word = kwargs['keyword']
        self.page = kwargs['page']

    def parse(self, response):
        print("test args: key_word", self.key_word)
        print("test args: page", self.page)
        pass

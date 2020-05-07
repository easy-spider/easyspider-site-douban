# -*- coding: utf-8 -*-
import scrapy


# TODO finish booksearch spider


class BooksearchSpider(scrapy.Spider):
    name = "booksearch"
    allowed_domains = ["https://book.douban.com/"]
    start_urls = ["http://https://book.douban.com//"]

    def parse(self, response):
        pass

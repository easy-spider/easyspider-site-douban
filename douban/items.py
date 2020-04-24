# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieTop250Item(scrapy.Item):
    ranking = scrapy.Field()  # 排名
    name = scrapy.Field()  # 电影名
    introduce = scrapy.Field()  # 简介
    star = scrapy.Field()  # 星级
    comments = scrapy.Field()  # 评论数
    describe = scrapy.Field()  # 描述


class MovieSearchItem(scrapy.Item):
    # 基本信息
    name = scrapy.Field()  # 电影名
    year = scrapy.Field()  # 年份
    director = scrapy.Field()  # 导演
    scriptwriter = scrapy.Field()  # 编剧
    leading_role = scrapy.Field()  # 主演
    style = scrapy.Field()  # 类型
    country = scrapy.Field()  # 国家/地区
    language = scrapy.Field()  # 语言
    release_time = scrapy.Field()  # 上映时间
    film_length = scrapy.Field()  # 片长
    alias = scrapy.Field()  # 别名
    imdb_link = scrapy.Field()  # IMDB链接

    # 介绍
    describe = scrapy.Field()  # 简介

    # 评价相关
    star = scrapy.Field()  # 星级
    evaluation = scrapy.Field()  # 评分人数
    comment = scrapy.Field()  # 短评数
    review = scrapy.Field()  # 长评数

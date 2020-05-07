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


class BookSearchItem(scrapy.Item):
    # 基本信息
    name = scrapy.Field()  # 书名
    writer = scrapy.Field()  # 作者
    publisher = scrapy.Field()  # 出版社
    producer = scrapy.Field()  # 出品方
    subhead = scrapy.Field()  # 副标题
    ori_name = scrapy.Field()  # 原名
    interpreter = scrapy.Field()  # 译者
    year = scrapy.Field()  # 出版年份
    pages = scrapy.Field()  # 页数
    price = scrapy.Field()  # 定价
    binding = scrapy.Field()  # 装帧
    series = scrapy.Field()  # 丛书
    isbn = scrapy.Field()  # ISBN

    # 介绍
    describe = scrapy.Field()  # 简介

    # 评价相关
    star = scrapy.Field()  # 星级
    evaluation = scrapy.Field()  # 评分人数
    comment = scrapy.Field()  # 短评数
    review = scrapy.Field()  # 长评数


class MusicSearchItem(scrapy.Item):
    # 基本信息
    name = scrapy.Field()  # 名称
    alias = scrapy.Field()  # 别名
    actor = scrapy.Field()  # 表演者
    genre = scrapy.Field()  # 流派
    type = scrapy.Field()  # 专辑类型
    media = scrapy.Field()  # 介质
    release_time = scrapy.Field()  # 发行时间
    publisher = scrapy.Field()  # 出版者
    cd_num = scrapy.Field()  # 唱片数
    bar_code = scrapy.Field()  # 条形码
    isrc = scrapy.Field()  # ISRC

    # 介绍
    describe = scrapy.Field()  # 简介

    # 曲目
    tracks = scrapy.Field()  # 曲目

    # 评价相关
    star = scrapy.Field()  # 星级
    evaluation = scrapy.Field()  # 评分人数
    comment = scrapy.Field()  # 短评数
    review = scrapy.Field()  # 长评数

# -*- coding: utf-8 -*-
import scrapy
from douban.items import MovieSearchItem


# TODO finsh DouBan Search crawl

class MoviesearchSpider(scrapy.Spider):
    name = 'moviesearch'
    allowed_domains = ['movie.douban.com']
    # start_urls = ['http://movie.douban.com/']
    # start_urls = ['https://movie.douban.com/subject/30211998/']
    # start_urls = ['https://movie.douban.com/subject/1292052/']
    # start_urls = ['https://movie.douban.com/subject/33411505/?tag=%E7%83%AD%E9%97%A8&from=gaia']
    # start_urls = ['https://movie.douban.com/subject/1924599/']
    start_urls = ['https://movie.douban.com/subject/1291546/']

    def __init__(self, **kwargs):
        self.key_word = kwargs['keyword']
        self.page = kwargs['page']

    def parse(self, response):
        # print("test args: key_word", self.key_word)
        # print("test args: page", self.page)
        # 基本信息
        item = MovieSearchItem()

        item['name'] = ''
        name = response.xpath("//*[@id='content']/h1/span[1]/text()").extract_first()
        if name is not None:
            item['name'] = name

        item['year'] = ''
        year = response.xpath("//*[@id='content']/h1/span[2]/text()").extract_first()
        if year is not None:
            item['year'] = year[1:len(year) - 1]

        item['director'] = ''
        director = response.xpath("//*[@id='info']/span[1]/span[2]/a/text()").extract_first()
        if director is not None:
            item['director'] = director

        item['scriptwriter'] = ''
        scriptwriters = response.xpath("//*[@id='info']/span[2]/span[2]//a[@href]/text()").extract()
        for writer in scriptwriters:
            item['scriptwriter'] += writer + ' '

        item['leading_role'] = ''
        leading_roles = response.xpath("//*[@id='info']/span[3]/span[2]//a[@rel='v:starring']/text()").extract()
        for role in leading_roles:
            item['leading_role'] += role + ' '

        item['style'] = ''
        styles = response.xpath("//*[@id='info']/span[@property='v:genre']/text()").extract()
        for s in styles:
            item['style'] += s + ' '

        item['country'] = ''
        item['language'] = ''
        item['alias'] = ''
        info_text = response.xpath("//*[@id='info']/text()").extract()
        # print("info_text_1", info_text)
        info_text = [info_text[i] for i in range(0, len(info_text)) if '\n' not in info_text[i] and
                     info_text[i] != ' / ' and info_text[i] != ' ']
        # print("info_text_2", info_text)
        info_text_set = []
        index = 0
        while len(info_text) > 0:
            info_text_set.append('')
            element = info_text.pop(0)
            for s in element.split(' / '):
                info_text_set[index] += s + ' '
            index += 1
        if len(info_text_set[0]) > 1:
            item['country'] = info_text_set[0][1:]
        if len(info_text_set[1]) > 1:
            item['language'] = info_text_set[1][1:]
        for i in range(2, len(info_text_set)):
            if '分钟' not in info_text_set[i]:
                if len(info_text_set[i]) > 1:
                    item['alias'] = info_text_set[i][1:]
                break

        item['film_length'] = ''
        film_length = response.xpath("//*[@id='info']/span[@property='v:runtime']/text()").extract_first()
        if film_length is not None:
            item['film_length'] = film_length

        item['imdb_link'] = ''
        imbd_link = response.css('#info > a[href^="https://www.imdb.com/title/"]::text').extract_first()
        if imbd_link is not None:
            item['imdb_link'] = 'https://www.imdb.com/title/' + imbd_link

        # print("name:", item['name'])
        # print("year:", item['year'])
        # print("director:", item['director'])
        # print("scriptwriter:", item['scriptwriter'])
        # print("leading_role:", item['leading_role'])
        # print("style:", item['style'])
        # print("country:", item['country'])
        # print("language:", item['language'])
        # print("alias:", item['alias'])
        # print("film_length:", item['film_length'])
        # print("imdb_link", item['imdb_link'])

        # 介绍
        # //*[@id="link-report"]/span[2]/text()[2]
        item['describe'] = ''
        describe_summary = response.xpath("//*[@id='content']//span[@property='v:summary']/text()").extract_first()
        describe_hidden = response.xpath("//*[@id='content']//span[@class='all hidden']/text()").extract()
        if len(describe_hidden) != 0:
            # print("describe_hidden not None", describe_hidden)
            for describe in describe_hidden:
                for s in describe.split():
                    item['describe'] += s
        elif describe_summary is not None:
            for s in describe_summary.split():
                item['describe'] += s

        # print("describe:", item['describe'])

        # 评价相关
        item['star'] = ''
        star = response.xpath("//*[@id='interest_sectl']/div[1]/div[2]/strong/text()").extract_first()
        if star is not None:
            item['star'] = star

        item['evaluation'] = '0'
        evaluation = response.xpath("//*[@id='interest_sectl']/div[1]/div[2]/div/div[2]/a/span/text()").extract_first()
        if evaluation is not None:
            item['evaluation'] = evaluation

        item['comment'] = '0'
        comment = response.xpath("//*[@id='comments-section']/div[1]/h2/span/a//text()").extract_first()
        if comment is not None:
            item['comment'] = comment.split()[1]

        item['review'] = '0'
        review = response.xpath("//*[@id='content']/div[@class='grid-16-8 clearfix']/div["
                                "1]/section/header/h2/span/a/text()").extract_first()
        if review is not None:
            item['review'] = review.split()[1]

        # print("star:", item['star'])
        # print("evaluation:", item['evaluation'])
        # print("comment:", item['comment'])
        # print("review:", item['review'])

        yield item

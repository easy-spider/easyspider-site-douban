# -*- coding: utf-8 -*-
import scrapy
from douban.items import MovieSearchItem

# TODO finsh DouBan Search crawl

class MoviesearchSpider(scrapy.Spider):
    name = 'moviesearch'
    allowed_domains = ['movie.douban.com']
    # start_urls = ['http://movie.douban.com/']
    start_urls = ['https://movie.douban.com/subject/30211998/']

    def __init__(self, **kwargs):
        self.key_word = kwargs['keyword']
        self.page = kwargs['page']

    def parse(self, response):
        print("test args: key_word", self.key_word)
        print("test args: page", self.page)
        # 基本信息
        item = MovieSearchItem()

        item['name'] = response.xpath("//*[@id='content']/h1/span[1]/text()").extract_first()

        year = response.xpath("//*[@id='content']/h1/span[2]/text()").extract_first()
        item['year'] = year[1:len(year)-1]

        item['director'] = response.xpath("//*[@id='info']/span[1]/span[2]/a/text()").extract_first()

        scriptwriters = response.xpath("//*[@id='info']/span[2]/span[2]//a[@href]/text()").extract()
        item['scriptwriter'] = ''
        for writer in scriptwriters:
            item['scriptwriter'] += writer+' '

        leading_roles = response.xpath("//*[@id='info']/span[3]/span[2]//a[@rel='v:starring']/text()").extract()
        item['leading_role'] = ''
        for role in leading_roles:
            item['leading_role'] += role+' '

        styles = response.xpath("//*[@id='info']/span[@property='v:genre']/text()").extract()
        item['style'] = ''
        for s in styles:
            item['style'] += s+' '

        info_text = response.xpath("//*[@id='info']/text()").extract()
        info_text = [info_text[i] for i in range(0, len(info_text)) if info_text[i] != '\n        ' and
                                                                       info_text[i] != ' ' and
                                                                       info_text[i] != ' ' and
                                                                       info_text[i] != ' / ' and
                                                                       info_text[i] != '\n\n' and
                                                                       info_text[i] != '\n        \n        ']

        item['country'] = ""
        for country in info_text[0].split(' / '):
            item['country'] += country+' '
        item['country'] = item['country'][1:len(item['country'])]

        item['language'] = ""
        for language in info_text[1].split(' / '):
            item['language'] += language+' '
        item['language'] = item['language'][1:len(item['language'])]

        item['alias'] = ""
        for language in info_text[2].split(' / '):
            item['alias'] += language+' '
        item['alias'] = item['alias'][1:len(item['alias'])]

        item['film_length'] = response.xpath("//*[@id='info']/span[@property='v:runtime']/text()").extract_first()

        item['imdb_link'] = response.css('#info > a[href^="https://www.imdb.com/title/"]::text').extract_first()
        item['imdb_link'] = 'https://www.imdb.com/title/'+item['imdb_link']

        # print("name:", item['name'])
        # print("year:", item['year'])
        # print("director:", item['director'])
        # print("scriptwriter:", item['scriptwriter'])
        # print("leading_role:", item['leading_role'])
        # print("style:", item['style'])
        # # print("info_text:", info_text)
        # print("country:", item['country'])
        # print("language:", item['language'])
        # print("alias:", item['alias'])
        # print("film_length:", item['film_length'])
        # print("imdb_link", item['imdb_link'])

        # 介绍
        describe = response.xpath("//*[@id='link-report']/span/text()").extract_first()
        item['describe'] = ''
        for s in describe.split():
            item['describe'] += s

        # print("describe:", item['describe'])

        # 评价相关
        item['star'] = response.xpath("//*[@id='interest_sectl']/div[1]/div[2]/strong/text()").extract_first()
        item['evaluation'] = response.xpath("//*[@id='interest_sectl']/div[1]/div[2]/div/div[2]/a/span/text()").\
            extract_first()

        comment = response.xpath("//*[@id='comments-section']/div[1]/h2/span/a//text()").extract_first()
        item['comment'] = comment.split()[1]

        review = response.xpath("//*[@id='content']/div[2]/div[1]/section/header/h2/span/a/text()").extract_first()
        item['review'] = review.split()[1]

        # print("star:", item['star'])
        # print("evaluation:", item['evaluation'])
        # print("comment:", item['comment'])
        # print("review:", item['review'])

        yield item




# -*- coding: utf-8 -*-
import scrapy
from douban.items import MovieSearchItem
from douban.custom_settings import movieSearchSetting
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from pydispatch import dispatcher
from scrapy import signals


# TODO Fix crawl TV series
# TODO Fix description(eg: '活着')


class MoviesearchSpider(scrapy.Spider):
    name = 'moviesearch'
    allowed_domains = ['movie.douban.com']
    # start_urls = ['http://movie.douban.com/']
    custom_settings = movieSearchSetting

    def __init__(self, **kwargs):
        # selenium setting
        self.page_timeout = self.custom_settings['SELENIUM_PAGE_TIMEOUT']
        self.element_timeout = self.custom_settings['SELENIUM_ELEMENT_TIMEOUT']
        self.isLoadImage = self.custom_settings['LOAD_IMAGE']
        self.windowHeight = self.custom_settings['WINDOW_HEIGHT']
        self.windowWidth = self.custom_settings['WINDOW_WIDTH']
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        self.browser = webdriver.Chrome(chrome_options=options)
        # self.browser = webdriver.Chrome()
        if self.windowHeight and self.windowWidth:
            self.browser.set_window_size(self.windowHeight, self.windowWidth)
        self.browser.set_page_load_timeout(self.page_timeout)  # 页面加载超时时间
        self.wait = WebDriverWait(self.browser, self.element_timeout)  # 指定元素加载超时时间

        # url from arguments
        self.key_word = kwargs['keyword']
        self.start_pos = str((int(kwargs['page']) - 1) * 15)
        self.search_result_url = 'https://search.douban.com/movie/subject_search?' + \
                                 'search_text=' + self.key_word + \
                                 '&start=' + self.start_pos

        dispatcher.connect(receiver=self.mySpiderCloseHandle,
                           signal=signals.spider_closed
                           )

    def mySpiderCloseHandle(self, spider):
        self.browser.quit()

    def start_requests(self):
        # print(self.search_result_url)
        return [scrapy.Request(self.search_result_url, meta={'usedSelenium': True, 'dont_redirect': False},
                               callback=self.parse_search_result)]

    def parse_search_result(self, response):
        movie_pages = response.css("div[class*='sc-bZQynM']")
        print("test: movie_pages size", len(movie_pages))
        for movie_page in movie_pages:
            # print("movie page:", movie_page)
            movie_page = movie_page.css("div.item-root a::attr(href)").extract_first()
            # print("movie page url:", movie_page)
            yield scrapy.Request(movie_page, callback=self.parse)

    def parse(self, response):
        # 基本信息
        self.logger.debug('start crawl movie page')
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

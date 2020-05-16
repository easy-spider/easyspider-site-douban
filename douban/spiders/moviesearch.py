# -*- coding: utf-8 -*-
import scrapy
from douban.items import MovieSearchItem
from douban.custom_settings import MovieSearchSetting
from douban.useragent import user_agent_list
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from pydispatch import dispatcher
from scrapy import signals
import random as rd


# TODO Fix crawl TV series


class MoviesearchSpider(scrapy.Spider):
    name = "moviesearch"
    allowed_domains = ["http://movie.douban.com"]
    custom_settings = MovieSearchSetting

    def __init__(self, **kwargs):
        # selenium setting
        self.page_timeout = self.custom_settings["SELENIUM_PAGE_TIMEOUT"]
        self.element_timeout = self.custom_settings["SELENIUM_ELEMENT_TIMEOUT"]
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument(f"--user-agent={rd.choice(user_agent_list)}")
        self.browser, self.wait = None, None

        # url from arguments
        self.key_word = kwargs["keyword"]
        self.start_pos = str((int(kwargs["page"]) - 1) * 15)
        self.search_result_url = (
            "https://search.douban.com/movie/subject_search?"
            + "search_text="
            + self.key_word
            + "&start="
            + self.start_pos
        )

        # spider关闭时，退出browser
        dispatcher.connect(
            receiver=self.mySpiderCloseHandle, signal=signals.spider_closed
        )

    def mySpiderCloseHandle(self, spider):
        self.browser.quit()

    def start_requests(self):
        self.logger.debug("Find an available proxy ip")
        return [
            scrapy.Request(
                self.search_result_url,
                meta={"test_timeout": True, "dont_redirect": True},
                callback=self.parse_test_result,
            )
        ]

    def parse_test_result(self, response):
        result = response.xpath(
            '//a[@href="https://movie.douban.com"]/text()'
        ).extract_first()
        self.logger.debug(f"parse verify response {response.url}, get text {result}")
        if result is None:
            self.logger.debug("Invalid Proxy IP")
            return [
                scrapy.Request(
                    response.url,
                    meta={
                        "test_timeout": True,
                        "invalid_Proxy": True,
                        "dont_redirect": True,
                    },
                    callback=self.parse_test_result,
                    dont_filter=True,
                )
            ]
        else:
            self.logger.debug("Verify proxy passed, start search request")
            self.logger.debug(
                f"Apply proxy and start chrome, proxy https:{response.meta['proxy']}"
            )
            self.chrome_options.add_argument(
                "--proxy=" + "https:" + response.meta["proxy"]
            )
            self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
            self.browser.set_page_load_timeout(self.page_timeout)  # 页面加载超时时间
            self.wait = WebDriverWait(self.browser, self.element_timeout)  # 指定元素加载超时时间
            return [
                scrapy.Request(
                    self.search_result_url,
                    meta={"usedSelenium": True, "dont_redirect": False},
                    callback=self.parse_search_result,
                    dont_filter=True,
                )
            ]

    def parse_search_result(self, response):
        self.logger.debug(f"start request {self.search_result_url}")
        movie_pages = response.css("div[class*='sc-bZQynM']")
        for movie_page in movie_pages:
            movie_page = movie_page.css("div.item-root a::attr(href)").extract_first()
            yield scrapy.Request(
                movie_page,
                meta={"dont_redirect": True},
                callback=self.parse,
                dont_filter=True,
            )

    def parse(self, response):
        # 基本信息
        self.logger.debug(f"start crawl movie page {response.url}")
        item = MovieSearchItem()

        item["name"] = ""
        name = response.xpath("//*[@id='content']/h1/span[1]/text()").extract_first()
        if name is not None:
            item["name"] = name

        item["year"] = ""
        year = response.xpath("//*[@id='content']/h1/span[2]/text()").extract_first()
        if year is not None:
            item["year"] = year[1 : len(year) - 1]

        item["director"] = ""
        director = response.xpath(
            "//*[@id='info']/span[1]/span[2]/a/text()"
        ).extract_first()
        if director is not None:
            item["director"] = director

        item["scriptwriter"] = ""
        scriptwriters = response.xpath(
            "//*[@id='info']/span[2]/span[2]//a[@href]/text()"
        ).extract()
        for writer in scriptwriters:
            item["scriptwriter"] += writer + " "

        item["leading_role"] = ""
        leading_roles = response.xpath(
            "//*[@id='info']/span[3]/span[2]//a[@rel='v:starring']/text()"
        ).extract()
        for role in leading_roles:
            item["leading_role"] += role + " "

        item["style"] = ""
        styles = response.xpath(
            "//*[@id='info']/span[@property='v:genre']/text()"
        ).extract()
        for s in styles:
            item["style"] += s + " "

        item["country"] = ""
        item["language"] = ""
        item["alias"] = ""
        info_text = response.xpath("//*[@id='info']/text()").extract()
        info_text = [
            info_text[i]
            for i in range(0, len(info_text))
            if "\n" not in info_text[i]
            and info_text[i] != " / "
            and info_text[i] != " "
        ]

        info_text_set = []
        index = 0
        while len(info_text) > 0:
            info_text_set.append("")
            element = info_text.pop(0)
            for s in element.split(" / "):
                info_text_set[index] += s + " "
            index += 1
        if len(info_text_set[0]) > 1:
            item["country"] = info_text_set[0][1:]
        if len(info_text_set[1]) > 1:
            item["language"] = info_text_set[1][1:]
        for i in range(2, len(info_text_set)):
            if "分钟" not in info_text_set[i]:
                if len(info_text_set[i]) > 1:
                    item["alias"] = info_text_set[i][1:]
                break

        item["film_length"] = ""
        film_length = response.xpath(
            "//*[@id='info']/span[@property='v:runtime']/text()"
        ).extract_first()
        if film_length is not None:
            item["film_length"] = film_length

        item["imdb_link"] = ""
        imbd_link = response.css(
            '#info > a[href^="https://www.imdb.com/title/"]::text'
        ).extract_first()
        if imbd_link is not None:
            item["imdb_link"] = "https://www.imdb.com/title/" + imbd_link

        # 介绍
        item["describe"] = ""
        describe_summarys = response.xpath(
            "//*[@id='content']//span[@property='v:summary']/text()"
        ).extract()
        describe_hidden = response.xpath(
            "//*[@id='content']//span[@class='all hidden']/text()"
        ).extract()
        describe = ""
        if len(describe_hidden) != 0:
            describe = describe_hidden
        elif describe_summarys is not None:
            describe = describe_summarys
        for i in range(0, len(describe)):
            describe[i] = "".join(describe[i].split("\u3000\u3000"))
            describe[i] = "".join(describe[i].split("\n"))
            describe[i] = "".join(describe[i].split())
        item["describe"] += " ".join(
            [describe[i] for i in range(0, len(describe)) if describe[i] != ""]
        )

        # 评价相关
        item["star"] = ""
        star = response.xpath(
            "//*[@id='interest_sectl']/div[1]/div[2]/strong/text()"
        ).extract_first()
        if star is not None:
            item["star"] = star

        item["evaluation"] = "0"
        evaluation = response.xpath(
            "//*[@id='interest_sectl']/div[1]/div[2]/div/div[2]/a/span/text()"
        ).extract_first()
        if evaluation is not None:
            item["evaluation"] = evaluation

        item["comment"] = "0"
        comment = response.xpath(
            "//*[@id='comments-section']/div[1]/h2/span/a//text()"
        ).extract_first()
        if comment is not None:
            item["comment"] = comment.split()[1]

        item["review"] = "0"
        review = response.xpath(
            "//*[@id='content']/div[@class='grid-16-8 clearfix']/div["
            "1]/section/header/h2/span/a/text()"
        ).extract_first()
        if review is not None:
            item["review"] = review.split()[1]

        yield item

# -*- coding: utf-8 -*-
import scrapy
from douban.items import MusicSearchItem
from douban.custom_settings import MusicSearchSetting
from douban.useragent import user_agent_list
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from pydispatch import dispatcher
from scrapy import signals
import random as rd


class MusicsearchSpider(scrapy.Spider):
    name = "musicsearch"
    allowed_domains = ["music.douban.com"]
    custom_settings = MusicSearchSetting

    def __init__(self, **kwargs):
        # selenium setting
        self.field = self.custom_settings["FIELD"]
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
            "https://search.douban.com/music/subject_search?"
            + "search_text="
            + self.key_word
            + "&start="
            + self.start_pos
        )

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
            '//a[@href="https://music.douban.com"]/text()'
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
        self.logger.debug("start crawl music page")
        item = MusicSearchItem()

        item["name"] = ""
        name = response.xpath('//*[@id="wrapper"]/h1/span/text()').extract_first()
        if name is not None:
            item["name"] = name

        info = response.xpath('//div[@id="info"]//text()').extract()
        for i in range(0, len(info)):
            info[i] = "".join(info[i].split("\n"))
            info[i] = "".join(info[i].split())
        info = [
            info[i] for i in range(0, len(info)) if info[i] != "" and info[i] != ":"
        ]

        for field in self.field:
            item[field[0]] = ""
            index = -1
            for i in range(0, len(info), 2):
                if field[1] in info[i]:
                    index = i + 1
                    break
            if index != -1:
                item[field[0]] = info[index]

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
            describe[i] = "".join(
                [
                    describe[i].split()[j]+' ' for j in range(len(describe[i].split()))
                ]
            )
        item["describe"] += " ".join(
            [describe[i] for i in range(0, len(describe)) if describe[i] != ""]
        )

        # 曲目
        item["tracks"] = ""
        track_list = response.xpath('//div[@class="track-list"]//text()').extract()
        for i in range(0, len(track_list)):
            track_list[i] = "".join(track_list[i].split("\n"))
            track_list[i] = "".join(track_list[i].split()) + "\n"
        item["tracks"] = "".join(
            [track_list[i] for i in range(0, len(track_list)) if track_list[i] != "\n"]
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
            '//*[@id="content"]/div/div[1]/div[3]/div[6]/h2/span/a//text()'
        ).extract_first()
        if comment is not None:
            item["comment"] = comment.split()[1]

        item["review"] = "0"
        review = response.xpath(
            '//*[@id="content"]/div/div[1]/div[3]/section/header/h2/span/a/text()'
        ).extract_first()
        if review is not None:
            item["review"] = review.split()[1]

        yield item

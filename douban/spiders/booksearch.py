# -*- coding: utf-8 -*-
import scrapy
from douban.items import BookSearchItem
from douban.custom_settings import BookSearchSetting
from douban.useragent import user_agent_list
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from pydispatch import dispatcher
from scrapy import signals
import random as rd


class MusicsearchSpider(scrapy.Spider):
    name = "booksearch"
    allowed_domains = ["book.douban.com"]
    custom_settings = BookSearchSetting

    def __init__(self, **kwargs):
        # selenium setting
        self.page_timeout = self.custom_settings["SELENIUM_PAGE_TIMEOUT"]
        self.element_timeout = self.custom_settings["SELENIUM_ELEMENT_TIMEOUT"]
        self.field = self.custom_settings["FIELD"]
        user_agent = rd.choice(user_agent_list)
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-infobars")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--user-agent={user_agent}")
        self.browser = webdriver.Chrome(chrome_options=options)
        self.browser.set_page_load_timeout(self.page_timeout)  # 页面加载超时时间
        self.wait = WebDriverWait(self.browser, self.element_timeout)  # 指定元素加载超时时间

        # url from arguments
        self.key_word = kwargs["keyword"]
        self.start_pos = str((int(kwargs["page"]) - 1) * 15)
        self.search_result_url = (
            "https://search.douban.com/book/subject_search?"
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
        self.logger.debug(f"start request {self.search_result_url}")
        return [
            scrapy.Request(
                self.search_result_url,
                meta={"usedSelenium": True, "dont_redirect": False},
                callback=self.verify_proxy_ip,
            )
        ]

    def verify_proxy_ip(self, response):
        self.logger.debug("verify response")
        movie_pages = response.css("div[class*='sc-bZQynM']")
        if len(movie_pages) > 0:
            test_url = movie_pages[0].css("div.item-root a::attr(href)").extract_first()
            self.logger.debug(f"test url {response.url}")
            return [
                scrapy.Request(
                    test_url,
                    meta={"test_timeout": True, "dont_redirect": True},
                    callback=self.parse_test_result,
                )
            ]

    def parse_test_result(self, response):
        if response.xpath('//*[@id="wrapper"]/h1/span/text()').extract_first() is None:
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
            self.logger.debug("Verify proxy passed, start parse search result")
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
                movie_page, meta={"dont_redirect": True}, callback=self.parse
            )

    def parse(self, response):
        self.logger.debug("start crawl book page")
        item = BookSearchItem()
        # 基本信息
        item["name"] = ""
        name = response.xpath('//*[@id="wrapper"]/h1/span/text()').extract()
        if name is not None:
            item["name"] = name[0]

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
            for i in range(0, len(info)):
                if field[1] in info[i]:
                    index = i + 1
                    break
            if index != -1:
                item[field[0]] = info[index]

        # 介绍
        describe_summarys = response.xpath(
            "//*[@id='content']//div[@id='link-report']//div[@class='intro'][1]//text()"
        ).extract()
        describe_hidden = response.xpath(
            "//*[@id='content']//div[@id='link-report']//span[@class='all hidden']//div[@class='intro']//text()"
        ).extract()
        item["describe"] = ""
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

        writer_describe_summarys = response.xpath(
            "//*[@id='content']//div[@class='related_info']//div[contains(@class,'indent')][2]//div["
            "@class='intro'][1]//text()"
        ).extract()
        writer_describe_hidden = response.xpath(
            "//*[@id='content']//div[@class='related_info']//div[contains(@class,'indent')][2]//span[@class='all "
            "hidden']//div[ "
            "@class='intro']//text()"
        ).extract()
        item["writer_describe"] = ""
        describe = ""
        if len(writer_describe_hidden) != 0:
            describe = writer_describe_hidden
        elif writer_describe_summarys is not None:
            describe = writer_describe_summarys
        for i in range(0, len(describe)):
            describe[i] = "".join(describe[i].split("\u3000\u3000"))
            describe[i] = "".join(describe[i].split("\n"))
            describe[i] = "".join(describe[i].split())
        item["writer_describe"] += " ".join(
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
            '//*[@id="interest_sectl"]/div/div[2]/div/div[2]/span/a/span/text()'
        ).extract_first()
        if evaluation is not None:
            item["evaluation"] = evaluation

        item["comment"] = "0"
        comment = response.xpath(
            '//*[@id="content"]//div[@class="mod-hd"]//span[@class="pl"]/a/text()'
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

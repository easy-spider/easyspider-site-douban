import sys
sys.path.append("/home/icespark/project/py/easyspider-site-douban/")
from unittest import TestCase
from douban.spiders.musicsearch import MusicsearchSpider
from douban.middlewares import SeleniumMiddleware
from scrapy.http import TextResponse, Request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import requests


class TestMusicsearchSpider(TestCase):
    spider = MusicsearchSpider(keyword="陈奕迅", page=1)
    seleniumMiddleware = SeleniumMiddleware()

    def test_start_requests(self):
        true_result = self.spider.start_requests()
        self.assertTrue(true_result[0].meta["test_timeout"] is True)

    def test_parse_test_result(self):
        true_response = online_response_from_url(
            "https://search.douban.com/music/subject_search?search_text=%E9%99%88%E5%A5%95%E8%BF%85&cat=1003",
        )
        false_response = online_response_from_url("http://www.baidu.com",)
        try:
            true_test_result = self.spider.parse_test_result(true_response)
            false_test_result = self.spider.parse_test_result(false_response)
        except Exception as e:
            print(f"test_parse_test_result exception: {e}")
            self.assertTrue(False)
        else:
            print("true_test_result", true_test_result[0].meta)
            print("false_test_result", false_test_result[0].meta)
            self.assertTrue(true_test_result[0].meta["usedSelenium"] is True)
            self.assertTrue(false_test_result[0].meta["invalid_Proxy"] is True)

    def test_parse_search_result(self):
        true_url = "https://search.douban.com/music/subject_search?search_text=%E9%99%88%E5%A5%95%E8%BF%85&cat=1003"
        false_url = "https://www.baidu.com"
        heads = {
            "User-Agent": "Mozilla/5.0 "
            "(Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 "
            "(KHTML, like Gecko) Version/5.1 Safari/534.50"
        }
        self.spider.browser = webdriver.Chrome(
            chrome_options=self.spider.chrome_options
        )
        self.spider.browser.set_page_load_timeout(self.spider.page_timeout)  # 页面加载超时时间
        self.spider.wait = WebDriverWait(
            self.spider.browser, self.spider.element_timeout
        )  # 指定元素加载超时时间
        true_request = Request(
            url=true_url,
            headers=heads,
            meta={"usedSelenium": True, "dont_redirect": False},
        )
        false_request = Request(
            url=false_url,
            headers=heads,
            meta={"usedSelenium": True, "dont_redirect": False},
        )
        true_response = self.seleniumMiddleware.process_request(
            true_request, self.spider
        )
        false_response = self.seleniumMiddleware.process_request(
            false_request, self.spider
        )
        # with open("./response.html", "wb+") as f:
        #     f.write(true_response.body)
        try:
            true_test_result = self.spider.parse_search_result(true_response)
            false_test_result = self.spider.parse_search_result(false_response)
        except Exception as e:
            print(f"test_parse_search_result exception: {e}")
            self.assertTrue(False)
        else:
            true_count, false_count = 0, 0
            while True:
                try:
                    print("true_test_result:", next(true_test_result).meta)
                    true_count += 1
                except StopIteration:
                    break
            while True:
                try:
                    print(next(false_test_result).meta)
                    false_count += 1
                except StopIteration:
                    break
            self.assertTrue(true_count == 15)
            self.assertTrue(false_count == 0)

    def test_parse(self):
        true_response = online_response_from_url(
            "https://music.douban.com/subject/6844753/"
        )
        false_response = online_response_from_url("https://www.baidu.com")

        try:
            true_item = next(self.spider.parse(true_response))
            self.assertTrue(true_item["name"] is not None)
        except StopIteration:
            print("get true_item fail")
            self.assertTrue(False)

        try:
            false_item = next(self.spider.parse(false_response))
        except Exception as e:
            print(f"get false_item exception {e}")
            self.assertTrue(True)
        else:
            self.assertTrue(false_item["name"] is not None)


def online_response_from_url(url=None, proxy=""):
    if not url:
        url = "http://book.douban.com"
    heads = {
        "User-Agent": "Mozilla/5.0 "
        "(Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 "
        "(KHTML, like Gecko) Version/5.1 Safari/534.50"
    }
    request = Request(url=url, headers=heads, meta={"proxy": proxy})
    oresp = requests.get(url, headers=heads)

    response = TextResponse(url=url, headers=heads, body=oresp.content, request=request)

    # with open("./response.html", "wb+") as f:
    #     f.write(response.body)
    return response

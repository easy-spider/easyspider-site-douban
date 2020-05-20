import sys
sys.path.append("/home/icespark/project/py/easyspider-site-douban/")

from unittest import TestCase
from douban.middlewares import RandomProxyMiddleware, SeleniumMiddleware, user_agent
from douban.spiders.moviesearch import MoviesearchSpider
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class TestRandomProxyMiddleware(TestCase):
    randomProxyMiddleware = RandomProxyMiddleware()
    spider = MoviesearchSpider(keyword="诺兰", page=1)

    url = 'https://movie.douban.com/'
    heads = {
        "User-Agent": "Mozilla/5.0 "
                      "(Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 "
                      "(KHTML, like Gecko) Version/5.1 Safari/534.50"
    }
    request = Request(url=url, headers=heads, meta={"invalid_Proxy": True, 'test_timeout': True})

    def test_process_request(self):
        self.randomProxyMiddleware.process_request(self.request, self.spider)
        self.assertTrue(self.request.meta['proxy'] is not None)


class TestSeleniumMiddleware(TestCase):
    seleniumMiddleware = SeleniumMiddleware()
    spider = MoviesearchSpider(keyword="诺兰", page=1)

    url = 'https://search.douban.com/movie/subject_search?search_text=%E8%AF%BA%E5%85%B0&cat=1002'
    heads = {
        "User-Agent": "Mozilla/5.0 "
                      "(Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 "
                      "(KHTML, like Gecko) Version/5.1 Safari/534.50"
    }
    request = Request(url=url, headers=heads, meta={"usedSelenium": True, "dont_redirect": False})

    def test_process_request(self):
        self.spider.browser = webdriver.Chrome(
            chrome_options=self.spider.chrome_options
        )
        self.spider.browser.set_page_load_timeout(self.spider.page_timeout)  # 页面加载超时时间
        self.spider.wait = WebDriverWait(
            self.spider.browser, self.spider.element_timeout
        )
        response = self.seleniumMiddleware.process_request(self.request, self.spider)
        result = self.spider.parse_search_result(response)
        count = 0
        while True:
            try:
                print("true_test_result:", next(result).meta)
                count += 1
            except StopIteration:
                break
        self.assertTrue(count == 15)


class Testuser_agent(TestCase):
    useragentMiddleware = user_agent()
    spider = MoviesearchSpider(keyword="诺兰", page=1)

    url = 'https://search.douban.com/movie/subject_search?search_text=%E8%AF%BA%E5%85%B0&cat=1002'

    request = Request(url=url)

    def test_process_request(self):
        self.useragentMiddleware.process_request(self.request, self.spider)
        self.assertTrue(self.request.headers['USER_AGENT'] is not None)



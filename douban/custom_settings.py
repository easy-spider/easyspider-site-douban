movieTop250Setting = {
    "LOG_LEVEL": "INFO",
}

movieSearchSetting = {
    # 'LOG_LEVEL': 'INFO',
    "DOWNLOAD_DELAY": 3,
    "AUTOTHROTTLE_ENABLED": True,
    "DOWNLOADER_MIDDLEWARES": {
        # 代理中间件
        # 'mySpider.middlewares.ProxiesMiddleware': 400,
        # SeleniumMiddleware 中间件
        "douban.middlewares.SeleniumMiddleware": 543,
    },
    # "ITEM_PIPELINES": {"douban.pipelines.MongodbPipeline": 300},
    # ----------- selenium参数配置 -------------
    "SELENIUM_PAGE_TIMEOUT": 25,  # selenium浏览器的页面请求超时时间，单位秒
    "SELENIUM_ELEMENT_TIMEOUT": 25,  # selenium浏览器的元素请求超时时间，单位秒
}
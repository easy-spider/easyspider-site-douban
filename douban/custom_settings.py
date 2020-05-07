MovieSearchSetting = {
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

MusicSearchSetting = {
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
    "FIELD": [
        ["alias", "又名"],
        ["actor", "表演者"],
        ["genre", "流派"],
        ["type", "专辑类型"],
        ["media", "介质"],
        ["release_time", "发行时间"],
        ["publisher", "出版者"],
        ["cd_num", "唱片数"],
        ["bar_code", "条形码"],
        ["isrc", "ISRC(中国)"],
    ],
}

BookSearchSetting = {
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
    "FIELD": [
        ["writer", "作者"],
        ["publisher", "出版社"],
        ["producer", "出品方"],
        ["subhead", "副标题"],
        ["ori_name", "原作名"],
        ["interpreter", "译者"],
        ["year", "出版年"],
        ["pages", "页数"],
        ["price", "定价"],
        ["binding", "装帧"],
        ["series", "丛书"],
        ["isbn", "ISBN"],
    ],
}

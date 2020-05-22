import datetime


# to_day = datetime.datetime.now()

MovieSearchSetting = {
    # "LOG_LEVEL": 'DEBUG',
    # "LOG_FILE": f'log/moviesearch_{to_day.year}_{to_day.month}_{to_day.day}.log',
    "DOWNLOAD_DELAY": 0.5,  # 最低延时
    "AUTOTHROTTLE_ENABLED": True,  # 启动[自动限速]
    "AUTOTHROTTLE_DEBUG": True,  # 开启[自动限速]的debug
    "AUTOTHROTTLE_MAX_DELAY": 5,  # 设置最大下载延时
    "DOWNLOAD_TIMEOUT": 5,
    "CONCURRENT_REQUESTS_PER_DOMAIN": 4,  # 限制对该网站的并发请求数
    "DOWNLOADER_MIDDLEWARES": {
        # 代理中间件
        "douban.middlewares.RandomProxyMiddleware": 440,
        # SeleniumMiddleware 中间件
        "douban.middlewares.SeleniumMiddleware": 500,
        "douban.middlewares.user_agent": 543,
    },
    # "ITEM_PIPELINES": {"douban.pipelines.MongodbPipeline": 300},
    # ----------- selenium参数配置 -------------
    "SELENIUM_PAGE_TIMEOUT": 15,  # selenium浏览器的页面请求超时时间，单位秒
    "SELENIUM_ELEMENT_TIMEOUT": 15,  # selenium浏览器的元素请求超时时间，单位秒
    "FIELD": [
        ["director", "导演"],
        ["scriptwriter", "编剧"],
        ["leading_role", "主演"],
        ["style", "类型"],
        ["country", "制片国家/地区"],
        ["language", "语言"],
        ["release_time", "上映日期"],
        ["film_length", "片长"],
        ["alias", "又名"],
        ["imdb_link", "IMDb链接"],
    ],
}

MusicSearchSetting = {
    # "LOG_LEVEL": 'DEBUG',
    # "LOG_FILE": f'log/moviesearch_{to_day.year}_{to_day.month}_{to_day.day}.log',
    "DOWNLOAD_DELAY": 0.5,  # 最低延时
    "AUTOTHROTTLE_ENABLED": True,  # 启动[自动限速]
    "AUTOTHROTTLE_DEBUG": True,  # 开启[自动限速]的debug
    "AUTOTHROTTLE_MAX_DELAY": 5,  # 设置最大下载延时
    "DOWNLOAD_TIMEOUT": 5,
    "CONCURRENT_REQUESTS_PER_DOMAIN": 4,  # 限制对该网站的并发请求数
    "DOWNLOADER_MIDDLEWARES": {
        # 代理中间件
        "douban.middlewares.RandomProxyMiddleware": 440,
        # SeleniumMiddleware 中间件
        "douban.middlewares.SeleniumMiddleware": 500,
        "douban.middlewares.user_agent": 543,
    },
    # "ITEM_PIPELINES": {"douban.pipelines.MongodbPipeline": 300},
    # ----------- selenium参数配置 -------------
    "SELENIUM_PAGE_TIMEOUT": 15,  # selenium浏览器的页面请求超时时间，单位秒
    "SELENIUM_ELEMENT_TIMEOUT": 15,  # selenium浏览器的元素请求超时时间，单位秒
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
    # "LOG_LEVEL": 'DEBUG',
    # "LOG_FILE": f'log/moviesearch_{to_day.year}_{to_day.month}_{to_day.day}.log',
    "DOWNLOAD_DELAY": 0.5,  # 最低延时
    "AUTOTHROTTLE_ENABLED": True,  # 启动[自动限速]
    "AUTOTHROTTLE_DEBUG": True,  # 开启[自动限速]的debug
    "AUTOTHROTTLE_MAX_DELAY": 5,  # 设置最大下载延时
    "DOWNLOAD_TIMEOUT": 5,
    "CONCURRENT_REQUESTS_PER_DOMAIN": 4,  # 限制对该网站的并发请求数
    "DOWNLOADER_MIDDLEWARES": {
        # 代理中间件
        "douban.middlewares.RandomProxyMiddleware": 440,
        # SeleniumMiddleware 中间件
        "douban.middlewares.SeleniumMiddleware": 500,
        "douban.middlewares.user_agent": 543,
    },
    # "ITEM_PIPELINES": {"douban.pipelines.MongodbPipeline": 300},
    # ----------- selenium参数配置 -------------
    "SELENIUM_PAGE_TIMEOUT": 15,  # selenium浏览器的页面请求超时时间，单位秒
    "SELENIUM_ELEMENT_TIMEOUT": 15,  # selenium浏览器的元素请求超时时间，单位秒
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

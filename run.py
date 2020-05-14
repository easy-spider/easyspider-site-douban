from scrapy.cmdline import execute

# scrapy crawl moviesearch
# execute(
#     [
#         "scrapy",
#         "crawl",
#         "moviesearch",
#         "-akeyword=诺兰",
#         "-apage=1",
#         "-sMONGO_URL=mongodb://localhost:27017/",
#         "-sSPIDER_NAME=moviesearch",
#         "-sTASK_ID=001",
#         "-sJOB_ID=002",
#     ]
# )

# scrapy crawl movietop250
# execute(
#     [
#         "scrapy",
#         "crawl",
#         "movietop250",
#         "-sMONGO_URL=mongodb://localhost:27017/",
#         "-sSPIDER_NAME=movietop250",
#         "-sTASK_ID=001",
#         "-sJOB_ID=002",
#     ]
# )

# scrapy crawl musicsearch
execute(
    [
        "scrapy",
        "crawl",
        "musicsearch",
        "-akeyword=陈奕迅",
        "-apage=1",
        "-sMONGO_URL=mongodb://localhost:27017/",
        "-sSPIDER_NAME=musicsearch",
        "-sTASK_ID=001",
        "-sJOB_ID=002",
    ]
)

# scrapy crawl booksearch
# execute(
#     [
#         "scrapy",
#         "crawl",
#         "booksearch",
#         "-akeyword=刘慈欣",
#         "-apage=1",
#         "-sMONGO_URL=mongodb://localhost:27017/",
#         "-sSPIDER_NAME=booksearch",
#         "-sTASK_ID=001",
#         "-sJOB_ID=002",
#     ]
# )

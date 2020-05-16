from scrapy.cmdline import execute
import sys

if __name__ == "__main__":
    if len(sys.argv) <= 3:
        print("开始执行豆瓣 moviesearch 爬虫，默认关键词: 诺兰，默认页数: 1")
        execute(
            [
                "scrapy",
                "crawl",
                "moviesearch",
                "-akeyword=诺兰",
                "-apage=1",
                "-sMONGO_URL=mongodb://localhost:27017/",
                "-sSPIDER_NAME=moviesearch",
                "-sTASK_ID=001",
                "-sJOB_ID=002",
            ]
        )

        # print("开始执行豆瓣 musicsearch 爬虫，默认关键词: 陈奕迅，默认页数: 1")
        # execute(
        #     [
        #         "scrapy",
        #         "crawl",
        #         "musicsearch",
        #         "-akeyword=陈奕迅",
        #         "-apage=1",
        #         "-sMONGO_URL=mongodb://localhost:27017/",
        #         "-sSPIDER_NAME=musicsearch",
        #         "-sTASK_ID=001",
        #         "-sJOB_ID=002",
        #     ]
        # )

        # print("开始执行豆瓣 booksearch 爬虫，默认关键词: 刘慈欣，默认页数: 1")
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

    elif len(sys.argv) == 4:
        print(f"开始执行豆瓣 {sys.argv[1]} 爬虫，关键词:{sys.argv[2]}，页数: {sys.argv[3]}")
        execute(
            [
                "scrapy",
                "crawl",
                sys.argv[1],
                f"-akeyword={sys.argv[2]}",
                f"-apage={sys.argv[3]}",
                "-sMONGO_URL=mongodb://localhost:27017/",
                f"-sSPIDER_NAME={sys.argv[1]}",
                "-sTASK_ID=001",
                "-sJOB_ID=002",
            ]
        )

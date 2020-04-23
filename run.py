from scrapy.cmdline import execute

# scrapy crawl moviesearch
# execute(['scrapy', 'crawl', 'moviesearch', '-akeyword=icespark', '-apage=10', '-sMONGO_URL=mongodb://localhost:27017/', '-sSPIDER_NAME=moviesearch', '-sTASK_ID=001', '-sJOB_ID=002'])

# scrapy crawl movietop250
execute(['scrapy', 'crawl', 'movietop250', '-sMONGO_URL=mongodb://localhost:27017/', '-sSPIDER_NAME=movietop250',
         '-sTASK_ID=001', '-sJOB_ID=002'])

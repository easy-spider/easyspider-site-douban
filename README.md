# easyspider-site-douban
Scrapy scripts for douban movies, books and musics

An essential part of easyspider: https://github.com/easy-spider

Generalized from easyspider-template: https://github.com/easy-spider/easyspider-template

Deployed by easyspider-scheduler：https://github.com/easy-spider/easyspider-scheduler

Use mongodb as database to store resources

Use Proxy pool to deal with more anti crawler situation (optional)

## Branch
- 'master' branch is developed full function, including Proxy pool
- 'stable-without-proxypool' branch is quicker, more stable but without proxy pool

## Environment
- Ubuntu 16.04 / Other Linux release version
- Python 3.7.0 (anaconda3)
- Scrapy 2.0.1
- selenium 3.141.0
- scrapyd-client  1.1.0 
- pydispatcher	2.0.5
- pymongo 3.10.1
- coverage 5.0
- Google Chrome	80.0.3987.122 & chromediver (same version)
- Every environment request needed for https://github.com/Python3WebSpider/ProxyPool (only for proxy pool)
- Use "pip3 install -r requirements.txt" to quickly install environment(not including Chrome & Chromedriver)


## Run And Deployment
*** **It is not recommanded to run this repo respectively!** ***<br>
*** **If running in proxy pool mode, member to start Python3WebSpider/ProxyPool previously, and before that you need to "source env" first (For ProxyPool)** ***

- Run: <br>
> ./run.py [spider_name] [keyword] [pages] <br><br>
This will start to crawl resources from the website, according to the sipder and other arguments written in run.py. 

- Deployment: 
> ./build.sh <br><br>
This will generate an '*.egg' in folder ./release, what is for scrapyd to deploy

- unittest
> cd unit_test <br><br>
  ./unittest.sh <br><br>
This will start a unittest and generate report and html.(Proxypool required)

- Testbench
> ./testbench.py <br><br>
This will start a testbench according to the arguments inside the script

## What Is Available
- Crawl all kinds of info, like rankings, names, introductions, stars, comments, descriptions and so on
- Spider for movie search results
- Spider for book search results
- Spider for music search results

## TODO
- Support crawling for pictures and comments

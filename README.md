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
- Google Chrome	80.0.3987.122 & chromediver (Same Version)
- Every environment request needed for https://github.com/Python3WebSpider/ProxyPool (only for proxy pool)


## Run And Deployment
*** **It is not recommanded to run this repo respectively!** ***<br>
*** **If running in proxy pool mode, member to start Python3WebSpider/ProxyPool previously, and before that you need to "source env" first (For ProxyPool)** ***

- Run: <br>
> python run.py <br><br>
This will start to crawl resources from the website, according to the sipder and other arguments written in run.py. 

- Deployment: 
> ./build.sh <br><br>
This will generate an '*.egg' in folder ./release, what is for scrapyd to deploy

## What Is Available
- Crawl all kinds of movie info, like rankings, names, introductions, stars, comments, descriptions and so on
- Spider for Douban Top 250 movies
- Spider for movie search results
- Spider for book search results
- Spider for music search results

## TODO
- Support crawling for pictures and comments
- update moviesearch spider


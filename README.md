# easyspider-site-douban
An essential part of easyspider: https://github.com/easy-spider

(Should Be) Generalized from easyspider-template: https://github.com/easy-spider/easyspider-template


Scrapy scripts for douban movies, novels and musics, deployed by easyspider-scheduler

Use mongodb as database to store resources
## Environment
- Python 3.7.0 (anaconda3)
- Scrapy 2.0.1
- selenium 3.141.0
- scrapyd-client  1.1.0 
- pydispatcher	2.0.5
- pymongo 3.10.1
- Google Chrome	80.0.3987.122 & chromediver(same version)

## Run And Deployment
*It is not recommanded to run this repo respectively!*
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
- Pipeline to store resources into mongodb
- Use user_agent middleware to change useragent dynamically
- Design the argument interface for scrapyd
- Use Selenium to deal with JS elements
- Use custom_setting to different spiders

## TODO
- Spider for novel search results
- Spider for music search results
- Support local log storage
- Fix bugs in Spider for movie search results
- Extract template from this first Scrapy script
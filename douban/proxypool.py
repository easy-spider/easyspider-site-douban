import requests

proxypool_url = 'http://127.0.0.1:5555/random'
target_url = 'https://movie.douban.com/'


def get_random_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    return requests.get(proxypool_url).text.strip()


def proxy_test(url, proxy):
    """
    use proxy to crawl page
    :param url: page url
    :param proxy: proxy, such as 8.8.8.8:8888
    :return: html
    """
    proxies = {'http': 'http://' + proxy}
    return requests.get(url, proxies=proxies).text


proxy_pool = [
    "180.105.156.109:9999",
    "183.185.78.97:9797",
    "221.1.200.242:43399",
    "123.58.17.134:3128",
    "218.2.226.42:80"
]

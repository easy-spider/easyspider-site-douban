import requests

proxypool_url = "http://127.0.0.1:5555/random"
target_url = "https://movie.douban.com/"


def get_random_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    return requests.get(proxypool_url).text.strip()

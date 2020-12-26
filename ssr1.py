import requests
from urllib.parse import urljoin

from lxml import html

page_urls = [f'https://ssr1.scrape.center/page/{i}' for i in range(1, 11)]

base_url = 'https://ssr1.scrape.center/'


def get_tree(url: str):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree


def parse_one_movie(movie_url: str):
    info = dict()
    tree = get_tree(movie_url)
    info['title'] = tree.xpath(
        '/html/body/div/div[2]/div[1]/div/div/div[1]/div/div[2]/a/h2/text()')[0]
    score = tree.xpath(
        '/html/body/div/div[2]/div[1]/div/div/div[1]/div/div[3]/p[1]/text()')[0]
    info['score'] = float(score)
    info['intro'] = tree.xpath(
        '/html/body/div/div[2]/div[1]/div/div/div[1]/div/div[2]/div[4]/p/text()')[0]
    return info


def parse_one_page(page_url: str):
    tree = get_tree(page_url)
    movie_urls = tree.xpath(
        '/html/body/div/div[2]/div[1]/div[1]/div/div/div/div[2]/a/@href')
    for movie_url in movie_urls:
        yield urljoin(base_url, movie_url)


def parse_all():
    for page_url in page_urls:
        for movie_url in parse_one_page(page_url):
            yield parse_one_movie(movie_url)


if __name__ == "__main__":
    for movie in parse_all():
        print(movie)

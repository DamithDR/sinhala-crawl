# <a href="/news/sri-lanka">නවතම - ආරක්ෂක</a>
# <a href="/news/world-2">ජනපති - පාර්ලිමේන්තුව - අගමැති</a>
# <a href="/news/political-current-affairs">කාලීන සිදුවීම් සහ දේශපාලන</a>
# <a href="/news/world-3">සංවර්ධන - ආර්ථික</a>
# <a href="/news/entertainment">සංස්කෘතික සහ කලා</a>
# <a href="/news/world">විදෙස් - ක්‍රීඩා</a>
# <a href="/news/provincial-news"> දිස්ත්‍රික් සංවර්ධන පුවත්</a>
# <a href="/news/media-releases">මාධ්‍ය නිවේදන</a>
# <a href="/news/covid-19">COVID-19</a>
# <a href="/economy">ආර්ථික</a>
# <a href="/fetures">විශේෂාංග</a>
# <a href="/cabinet-decusions">කැබිනට් තීරණ</a>
# <a href="/reviews">විමර්ශන</a>
import os.path
import sys

import requests
from bs4 import BeautifulSoup

links = [
    # "/news/sri-lanka",
    # "/news/world-2",
    # "/news/political-current-affairs",
    # "/news/world-3",
    # "/news/entertainment",
    # "/news/world",
    # "/news/provincial-news",
    # "/news/media-releases",
    # "/news/covid-19",
    "/economy",
    "/fetures",
    "/cabinet-decusions",
    "/reviews"
]

categories = [
    # "local_news",
    # "president_parliament_prime_minister",
    # "political_current_affairs",
    # "development",
    # "cultural_and_arts",
    # "sports",
    # "provincial_news",
    # "media_releases",
    # "covid-19",
    "economy",
    "features",
    "cabinet-decisions",
    "reviews"
]

base_link = "https://sinhala.news.lk"
root_folder_path = 'data/sinhala_news_lk'

for category in categories:
    if not os.path.exists(f'{root_folder_path}/{category}'):
        os.mkdir(f'{root_folder_path}/{category}')


def extract_page_article_links(URL):
    print(f'extracting urls from : {URL}')
    payload = requests.get(URL, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})
    soup = BeautifulSoup(payload.content, "html.parser")
    full_links_list = set(soup.find_all("a", href=True))
    return [article_link['href'] for article_link in full_links_list if
            article_link['href'].startswith(f'{link}/item/')], soup


if __name__ == '__main__':
    try:
        for link, category in zip(links, categories):
            URL = base_link + link

            articles_links, soup = extract_page_article_links(URL)

            # print(articles_links)
            no_of_articles_per_page = len(articles_links)

            # find the last page start point
            last_page = soup.find_all("a", attrs={"title": "අවසානය"})
            last_page_start_number = int(last_page[0]['href'].split('?start=')[1])

            with open(f'{root_folder_path}/{category}/articles.txt', 'w') as file:
                file.writelines('\n'.join(articles_links))
                for i in range(no_of_articles_per_page, last_page_start_number, no_of_articles_per_page):
                    page_url = f"{URL}?start={i}"
                    articles_links, sp = extract_page_article_links(page_url)
                    file.writelines('\n'.join(articles_links))
    except:
        print(f'exception occured in link : {URL}')
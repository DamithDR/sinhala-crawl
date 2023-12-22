import json

import requests
from bs4 import BeautifulSoup, Tag

links = [
    "/news/sri-lanka",
    "/news/world-2",
    "/news/political-current-affairs",
    "/news/world-3",
    "/news/entertainment",
    "/news/world",
    "/news/provincial-news",
    "/news/media-releases",
    "/news/covid-19",
    "/economy",
    "/fetures",
    "/cabinet-decusions",
    "/reviews"
]

categories = [
    "local_news",
    "president_parliament_prime_minister",
    "political_current_affairs",
    "development",
    "cultural_and_arts",
    "sports",
    "provincial_news",
    "media_releases",
    "covid-19",
    "economy",
    "features",
    "cabinet-decisions",
    "reviews"
]

base_link = "https://sinhala.news.lk"
root_folder_path = 'data/sinhala_news_lk'
meta_path = 'metadata/sinhala_news_lk.meta'
if __name__ == '__main__':
    for link, category in zip(links, categories):
        news_article_number = 1
        with open(f'{root_folder_path}/{category}/articles.txt', 'r') as file:
            article_paths = list(set(file.readlines()))
            for article in article_paths:
                try:
                    article = article.replace('\n', '')
                    URL = f'{base_link}/{article}'
                    payload = requests.get(URL, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})
                    soup = BeautifulSoup(payload.content, "html.parser")
                    title = soup.find_all("h2", attrs={"class": "itemTitle"})
                    title = title[0].contents[0]
                    title = title.replace('\t', '').replace('\n', '')
                    date_time = soup.find_all("span", attrs={"class": "itemDateCreated"})
                    published_date = date_time[0].text
                    published_date = published_date.replace('\t', '').replace('\n', '')

                    item_intro = soup.find_all("div", attrs={"class": "itemIntroText"})
                    item_body = soup.find_all("div", attrs={"class": "itemFullText"})

                    full_text = item_intro[0].text.replace('\t', '').replace('\n', '') + '\n' + item_body[
                        0].text.replace('\t', '').replace('\n', '')

                    news_dict = {
                        "Source": base_link,
                        "Timestamp": published_date,
                        "Headline": title,
                        "News Content": full_text,
                        "URL": URL,
                        "Category": category
                    }

                    json_object = json.dumps(news_dict, indent=4, ensure_ascii=False)
                    with open(f'{root_folder_path}/{category}/{news_article_number}.json', "w",
                              encoding='utf8') as outfile:
                        outfile.write(json_object)
                    meta_string = f'processed category : {category} | article link : {link} | article_no : {news_article_number}'
                    print(meta_string)
                    with open(meta_path, 'a') as meta:
                        meta.write(meta_string + '\n')
                    news_article_number += 1
                except:
                    error_string = f'processed category : {category} | article link : {link}'
                    print(error_string)
                    with open(meta_path, 'a') as meta:
                        meta.write(error_string + '\n')

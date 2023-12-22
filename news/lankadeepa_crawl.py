import concurrent
import json
from concurrent.futures.thread import ThreadPoolExecutor

import requests
from bs4 import BeautifulSoup

categories = [
    "latest_news",
    "business",
    "politics",
    "features",
    "provincial-news",
    "deyyo_sakki"
]
root_folder_path = 'data/lankadeepa'
meta_path = 'metadata/lankadeepa.meta'


def crawl(links=[], start_index=0, category="temp", thread_no=0):
    print('crawling started ')

    for lnk in links:
        # l = 'https://www.lankadeepa.lk/news/%E0%B6%9A%E0%B7%9C%E0%B6%A7%E0%B7%92-%E0%B7%83%E0%B6%B8%E0%B6%BA%E0%B7%9A-%E0%B6%86%E0%B6%BA%E0%B7%94%E0%B6%B0-%E0%B6%BB%E0%B6%B1%E0%B7%8A-%E0%B7%83%E0%B7%9C%E0%B6%BA%E0%B7%8F-%E0%B6%9A%E0%B7%90%E0%B6%AB%E0%B7%93%E0%B6%B8%E0%B7%8A/101-641294'
        try:
            payload = requests.get(lnk, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})
            soup = BeautifulSoup(payload.content, "html.parser")

            titles = soup.find_all("h3", attrs={"class": "f1-l-3 cl2 p-b-0 respon2"})
            title = titles[0].text.replace('\t', '').replace('\n', '').replace('\r', '')
            date = soup.find_all('a', attrs={"class": "f1-s-4 cl8 hov-cl10 trans-03"})
            posted_date = date[0].text.replace('කතෘ මණ්ඩලය', '').replace('\t', '').replace('\n', '').replace('\r',
                                                                                                             '').strip()
            full_content = soup.find_all('div', attrs={"class": "header inner-content p-b-20"})
            full_text = full_content[0].text.replace('\t', '').replace('\n', '').replace('\r', '')
            news_dict = {
                "Source": "www.lankadeepa.lk",
                "Timestamp": posted_date,
                "Headline": title,
                "News Content": full_text,
                "URL": lnk,
                "Category": category
            }

            json_object = json.dumps(news_dict, indent=4, ensure_ascii=False)
            with open(f'{root_folder_path}/{category}/{thread_no}_{start_index}.json', "w",
                      encoding='utf8') as outfile:
                outfile.write(json_object)
            meta_string = f'Thread No : {thread_no} | processed category : {category} | article link : {lnk} | article_no : {start_index}'
            print(meta_string)
            with open(meta_path, 'a') as meta:
                meta.write(meta_string + '\n')
            start_index += 1
        except Exception as e:
            error_string = f'Thread No : {thread_no} | processed category : {category} | article link : {lnk} | error = {e}'
            print(error_string)
            with open(meta_path, 'a') as meta:
                meta.write(error_string + '\n')


if __name__ == '__main__':

    for category in categories:
        with open(f'{root_folder_path}/{category}/articles.txt', 'r') as file:
            links = file.readlines()
            links = [link.replace('\n', '') for link in links]
            chunk_size = int(len(links) / 4)
            # crawl(links[:chunk_size], 1, category)
            with ThreadPoolExecutor(max_workers=4) as executor:
                executor.submit(crawl, links[:chunk_size], 1, category, 1)
                executor.submit(crawl, links[chunk_size:chunk_size * 2], chunk_size + 1, category, 2)
                executor.submit(crawl, links[chunk_size * 2:chunk_size * 3], chunk_size * 2 + 1, category, 3)
                executor.submit(crawl, links[chunk_size * 3:], chunk_size * 3 + 1, category, 4)

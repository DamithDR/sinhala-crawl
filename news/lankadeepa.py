import os

import requests
from bs4 import BeautifulSoup

paths = {
    "latest_news": "https://www.lankadeepa.lk/latest-news/1",
    "business": "https://www.lankadeepa.lk/business/9",
    "politics": "https://www.lankadeepa.lk/politics/13",
    # "youth": "https://www.lankadeepa.lk/tharunaya/272",
    # "entertainment": "https://www.lankadeepa.lk/rasa-windana/239",
    "features": "https://www.lankadeepa.lk/features/2",
    "provincial-news": "https://www.lankadeepa.lk/provincial-news/59",
    "deyyo_sakki": "https://www.lankadeepa.lk/deyyo-sakki/15",
}

last_pages = {
    "latest_news": 122760,
    "business": 2100,
    "politics": 1230,
    # "youth": "https://www.lankadeepa.lk/tharunaya/272",
    # "entertainment": "https://www.lankadeepa.lk/rasa-windana/239",
    "features": 6720,
    "provincial-news": 15300,
    "deyyo_sakki": 3960,
}

base_link = "https://www.lankadeepa.lk/"
root_folder_path = 'data/lankadeepa'


def read_links(URL):
    payload = requests.get(URL, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})
    soup = BeautifulSoup(payload.content, "html.parser")
    articles = soup.find_all("a", attrs={"class": "f1-l-1 trans-03 respon2 malithi"})
    return [article['href'] for article in articles], soup

no_of_articles_per_page = 30

for category in paths.keys():
    print(f'processing category : {category}')
    if not os.path.exists(f'{root_folder_path}/{category}'):
        os.mkdir(f'{root_folder_path}/{category}')
    link = paths.get(category)
    ar_links, soup = read_links(link)
    print('\n'.join(ar_links))

    last_page_no = last_pages[category] + 10  # to take the last page

    with open(f'{root_folder_path}/{category}/articles.txt', 'w') as file:
        file.writelines('\n'.join(ar_links))
        for i in range(no_of_articles_per_page, last_page_no, no_of_articles_per_page):
            page_url = f"{link}/{i}"
            try:
                page_links, soup = read_links(page_url)
                file.write('\n')
                file.writelines('\n'.join(page_links))
                print('\n'.join(page_links))
            except:
                print(f'exception occured in :{page_url}')

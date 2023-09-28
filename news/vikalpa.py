import json
import os

import requests as requests
from bs4 import BeautifulSoup

no_of_pages = 350
news_article_number = 1
meta_path = 'metadata/vikalpa.meta'
if os.path.exists(meta_path):
    os.remove(meta_path)
source = "www.vikalpa.org"
for i in range(1, no_of_pages):

    # SEARCH_URL = "https://www.vikalpa.org/"
    URL = f"https://www.vikalpa.org/page/{i}"

    payload = requests.get(URL, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})

    soup = BeautifulSoup(payload.content, "html.parser")
    full_links_list = set(soup.find_all("a", href=True))

    all_contain_articles = [doc for doc in full_links_list if
                            doc['href'].startswith("https://www.vikalpa.org/article/")]

    news_articles = [article for article in all_contain_articles if len(article['href'].split("/article/")) == 2
                     and article['href'].split("/article/")[1].isnumeric()]

    for article in news_articles:
        # for article in news_articles:
        page_url = article['href']
        # page_url = 'https://www.vikalpa.org/article/42768'
        payload = requests.get(page_url, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})
        page = BeautifulSoup(payload.content, "html.parser")

        try:
            # read content
            title = page.find_all("h1", attrs={"class": "entry-title"})
            title = title[0].contents[0]['title']
            page_content = page.find_all("div", attrs={"class": "entry-content"})
            date_published = page.find_all("time", attrs={"class": "entry-date published"})
            published_date = date_published[0].contents[0]
            all_p = page_content[0].find_all('p')
            paragraphs = [p.text for p in all_p if not p.text.isascii()]
            news_dict = {
                "Source": source,
                "Timestamp": published_date,
                "Headline": title,
                "News Content": '\n'.join(paragraphs),
                "URL": page_url,
                "Category": "N/A"
            }
            json_object = json.dumps(news_dict, indent=4, ensure_ascii=False)
            with open(f"data/vikalpa/{news_article_number}.json", "w", encoding='utf8') as outfile:
                outfile.write(json_object)

            meta_string = f'processed page no {i}; article_no : {news_article_number}'
            print(meta_string)
            with open(meta_path, 'a') as meta:
                meta.write(meta_string + '\n')

            news_article_number += 1
        except:
            error_string = f'error occured in web_page_no: {i} in article: {page_url}'
            print(error_string)
            with open(meta_path, 'a') as meta:
                meta.write(error_string + '\n')

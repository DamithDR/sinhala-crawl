import requests
from bs4 import BeautifulSoup

base_path = "https://www.gossiplankanews.com"

article_list = []

for year in range(2016, 2024):
    for month in range(1, 13):
        URL = f'{base_path}/{year}/{month:02d}/'
        print(f'getting information from path : {URL}')
        payload = requests.get(URL, allow_redirects=True, headers={"User-Agent": "Chrome/102.0.0.0"})
        soup = BeautifulSoup(payload.content, "html.parser")
        articles = soup.find_all("a", attrs={"class": "read-more"})
        article_links = [a['href'] for a in articles]
        if len(article_links) > 0:
            article_list.extend(article_links)
        print(len(article_list))
with open('data/gossip_lanka/links.txt', 'w') as f:
    f.writelines('\n'.join(article_list))

import json
import time
from concurrent.futures.thread import ThreadPoolExecutor

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = True  # This enables headless mode
driver = webdriver.Chrome(options=options)
with open('data/gossip_lanka/links.txt', 'r') as file:
    links = file.readlines()
    index = 0
    for link in links:
        try:
            index += 1
            print(f'processing link : {link} | index : {index}')
            driver.get(link)
            driver.execute_script("window.scrollBy(0, 700);")
            try:
                anchor_tags = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//a[contains(text(), "reply") or contains(text(), "replies")]'))
                )

                for tag in anchor_tags:
                    if tag.accessible_name is not None:
                        tag.click()
            except Exception as exc:
                print(f"exception happened in link : {link}")
            time.sleep(1)
            page_source = driver.page_source

            soup = BeautifulSoup(page_source, 'html.parser')
            news_body = soup.find_all("div", attrs={"class": "post-body post-content"})
            news_body = news_body[0].text
            title = soup.find_all("h1", attrs={"class": "post-title"})
            title = title[0].text
            date = soup.find_all("span", attrs={"class": "post-date published"})
            date = date[0].text

            comments = []
            comment_treads = soup.find_all("div", attrs={"class": "idc-c idc-anonymous"})
            for thread in comment_treads:
                new_comment = {}
                likes = thread.findNext("span", attrs={"class", "idc-v-total"})
                likes = likes.text
                comment = thread.findNext("div", attrs={"class", "idc-c-t-inner"})
                new_comment['comment'] = comment.text
                new_comment['likes'] = likes
                comments.append(new_comment)

            news_dict = {
                "Source": "https://www.gossiplankanews.com/",
                "Timestamp": date,
                "Headline": title,
                "News Content": news_body,
                "URL": link,
                "Category": "N/A",
                "comments": comments
            }
            json_object = json.dumps(news_dict, indent=4, ensure_ascii=False)
            with open(f'data/gossip_lanka/data/{index}.json', "w",
                      encoding='utf8') as outfile:
                outfile.write(json_object)


        except Exception as e:
            print(f"exception in link {index}, : {e}")
driver.quit()

import json
import os

import requests
from bs4 import BeautifulSoup


def get_soup(url):
    response = requests.get(url=url)
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "lxml")


# json_dir = "json_files"
dir_path = os.path.join(os.getcwd(), "data/json_files")
#os.mkdir(dir_path)

file_path = os.path.join(dir_path, "test.json")
# url = "http://parsinger.ru/html/mouse/3/3_11.html"
# soup = get_soup(url)
# result_json = {
#     "name": soup.find("p", id="p_header").text,
#     "price": soup.find("span", id="price").text
# }

# url = "http://parsinger.ru/html/index3_page_1.html"
# soup = get_soup(url)
# names = [x.text.strip() for x in soup.find_all('a', class_='name_item')]
# descriptions = [x.text.strip().split('\n') for x in soup.find_all('div', class_='description')]
# prices = [x.text for x in soup.find_all('p', class_='price')]
# 
# result_json = []
# for description_item, price, name in zip(descriptions, prices, names):
#     result_json.append({
#         "name": name,
#         'brand': description_item[0].split(':')[1].strip(),
#         'type': description_item[1].split(':')[1].strip(),
#         'connect': description_item[2].split(':')[1].strip(),
#         'game': description_item[3].split(':')[1].strip(),
#         "price": price
#     })

url = "http://parsinger.ru/html/watch/1/1_1.html"
soup = get_soup(url)
description = soup.find("ul", id="description").find_all("li")
li_ids = [li.get("id") for li in description]
print(li_ids)

# with open(file_path, "w", encoding="utf-8") as file:
#     json.dump(result_json, file, indent=4, ensure_ascii=False)

# import io
# import os
# import zipfile

import requests
from bs4 import BeautifulSoup

# url = "https://parsinger.ru/downloads/cooking_soup/index.zip"
# zip_response = requests.get(url=url, stream=True)
# extract_dir = os.path.join(os.getcwd(), 'data')
# filenames = []
#
# with zipfile.ZipFile(io.BytesIO(zip_response.content)) as zf:
#     for file in zf.infolist():
#         zf.extract(file.filename, extract_dir)
#         filenames.append(file.filename)
#
# file_path = os.path.join(extract_dir, filenames[0])
#
# with open(file_path, 'r', encoding='utf-8') as file:
#     soup = BeautifulSoup(file, 'lxml')
#     print(soup)


# url = 'http://parsinger.ru/html/watch/1/1_1.html'
# response = requests.get(url=url)
# response.encoding = 'utf-8'
# print(response.text)

# soup = BeautifulSoup(response.text, 'lxml')
# print(soup.find('div'))

# url = "https://parsinger.ru/html/index1_page_1.html"
# url = "https://parsinger.ru/html/headphones/5/5_32.html"
url = "https://parsinger.ru/html/hdd/4/4_1.html"

response = requests.get(url=url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")
sale = soup.select("div.sale span")
old_price = float(sale[-1].text.split()[0])
new_price = float(sale[0].text.split()[0])
diff = old_price - new_price
discount = (diff / old_price) * 100
print(round(discount, 1))
# span = soup.find_all('p', 'price')
# total = 0
# for price in span:
#     total += int(price.text.split()[0])
# print([total := total + int(price.text.split()[0]) for price in span][-1])
# print(sum([int(price.text.split()[0]) for price in span]))
# p = soup.find('p', id='p_header')
# print(p.text)
# p = soup.find('p', 'article')
# print(type(p))
# print(p.text)
# print('\n'.join([li.text for li in soup.find('div', 'item').find_all('li')]))

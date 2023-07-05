import requests
from bs4 import BeautifulSoup
import csv

with open('res.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        'Наименование', 'Артикул', 'Бренд', 'Модель',
        'Наличие', 'Цена', 'Старая цена'])
url = 'https://parsinger.ru/html/index1_page_1.html'
response = requests.get(url=url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

pagen = int(soup.find('div', 'pagen').find_all('a')[-1].text)
category = [f"http://parsinger.ru/html/{x['href']}"
            for x in soup.find('div', 'nav_menu').find_all('a')]

print(len(soup.find('div', 'nav_menu').find_all('a')))
print(len(soup.find('div', 'pagen').find_all('a')))
import csv
import os

import requests
from bs4 import BeautifulSoup

csv_dir = "csv_files"
dir_path = os.path.join(os.getcwd(), "data/csv_files")
# os.mkdir(dir_path)

# new_file = "res.csv"
# new_file_path = os.path.join(dir_path, new_file)
# 
# lst = ["one", "two", "three"]
# 
# with open(new_file_path, "w", newline="", encoding="utf-8-sig") as file:
#     writer = csv.writer(file, delimiter=";")
#     writer.writerow(lst)

# url = "http://parsinger.ru/html/mouse/3/3_11.html"
# response = requests.get(url=url)
# response.encoding = "utf-8"
# soup = BeautifulSoup(response.text, "lxml")
# 
# name = soup.find('p', id='p_header').text
# article = soup.find('p', class_='article').text.split(': ')[1]
# brand = soup.find('li', id='brand').text.split(': ')[1]
# model = soup.find('li', id='model').text.split(': ')[1]
# type = soup.find('li', id='type').text.split(': ')[1]
# purpose = soup.find('li', id='purpose').text.split(': ')[1]
# light = soup.find('li', id='light').text.split(': ')[1]
# size = soup.find('li', id='size').text.split(': ')[1]
# dpi = soup.find('li', id='dpi').text.split(': ')[1]
# site = soup.find('li', id='site').text.split(': ')[1]
# in_stock = soup.find('span', id='in_stock').text.split(': ')[1]
# price = soup.find('span', id='price').text.split()[0]
# 
# file_name = "res_two.csv"
# new_file_path = os.path.join(dir_path, file_name)
# 
# with open(new_file_path, "a", newline="", encoding="utf-8-sig") as file:
#     writer = csv.writer(file, delimiter=";")
#     writer.writerow(
#         ['Наименование', 'Артикул', 'Бренд', 'Модель',
#         'Тип', 'Игровая', 'Размер', 'Подсветка', 'Разрешение',
#         'Сайт производителя', 'В наличии', 'Цена']
#     )
#     writer.writerow(
#         [name, article, brand, model,
#         type, purpose, size, light , dpi,
#         site, in_stock, price]
#     )

# url = "https://parsinger.ru/html/index3_page_2.html"
# response = requests.get(url=url)
# response.encoding = "utf-8"
# soup = BeautifulSoup(response.text, "lxml")
# 
# head = ['Наименование', 'Цена', 'Бренд', 'Тип', 'Подключение', 'Игровая']
# names = [
#     name_tag.text.strip() for name_tag in
#     soup.find_all("a", class_="name_item")
# ]
# prices = [
#     price_tag.text.strip() for price_tag in
#     soup.find_all("p", class_="price")
# ]
# descriptions = [
#     [
#         li.text.split(":")[1].strip() for li in
#         description.find_all("li") if li
#     ] for description in soup.find_all("div", class_="description")
# ]
# descriptions = [
#     [
#         value.split(":")[1].strip() for value in
#         block.text.split("\n") if value
#     ] for block in soup.find_all("div", class_="description")
# ]
# table_data = list(map(lambda x, y, z: (x, y, *z), names, prices, descriptions))
# file_name = "mouse_data.csv"
# new_file_path = os.path.join(dir_path, file_name)
# 
# with open(new_file_path, "w", newline="", encoding="utf-8-sig") as file:
#     writer = csv.writer(file, delimiter=";")
#     writer.writerow(head)
#     writer.writerows(table_data)


def get_soup(url):
    """
    Функция, создающая объект BeautifulSoup 
    на основе ответа запроса по указанной ссылке.

    Аргументы:
        :url - адреса запроса
    """
    response = requests.get(url=url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def parse_hdd_info(base_url, schema):
    """
    Функция постраничного парсинга информации
    о всех представленных на витрине hdd-диска.
    Возвращает список вложенных списков hdd_data,
    где hdd_data[0] - cписок названий параментров hdd-диска,
    а hdd_data[1:] - списки со значениями этих параметров для каждого hdd-диска.
    
    Аргументы:
        :base_url - url страницы для парсинга
                    относительных адресов страниц с hdd-дисками.
        :schema - базовая часть ссылки на страницу с витриной hdd-дисков.
    """
    HEADS = [
        "Наименование", "Бренд", "Форм-фактор",
        "Емкость", "Объём буф.памяти", "Цена"
    ]
    hdd_data = [HEADS]
    base_soup = get_soup(base_url)
    # находим элемент пагинации и создаём список ссылок на страницы с витринами
    pagen_tag = base_soup.find("div", class_="pagen")
    page_urls = [
        f"{schema}{a_tag['href']}" for a_tag in pagen_tag.find_all("a")
    ]
    # запускаем цикл постраничного парсинга данных о hdd-дисках
    for url in page_urls:
        page_soup = get_soup(url)
        # формируем список наименований 
        names = [
            name.text.strip() for name in
            page_soup.find_all("a", class_="name_item")
        ]
        # находим элементы с описанием hdd-дисков 
        description_tags = page_soup.find_all("div", class_="description")
        # формируем список с информацией о всех hdd-дисках на странице
        description_data = [
            [
                value.split(":")[1].strip() for value in
                hdd_item.text.split("\n") if value
            ] for hdd_item in description_tags
        ]
        # парсим список цен
        prices = [
            price.text.strip() for price in
            page_soup.find_all("p", class_="price")
        ]
        # склеиваем полученные списки, раскрывая вложенные в description_data,
        # и получаем список списков со всей информацией для каждого hdd-диска.
        page_data = list(
            map(lambda x, y, z: [x, *y, z], names, description_data, prices)
        )
        # добавляем информацию о дисках на странице в общую таблицу
        for row in page_data:
            hdd_data.append(row)

    return hdd_data


def list_to_csv(file_path, table_data):
    """
    Функция сохранения табличных данных в виде списка списков в csv-файл.

    Аргументы:
        :file_path - адрес csv-файла, куда производится запись данных.
        :table_data - данные 'iterable of rows' объекта для записи в csv-файл.
    """
    with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(table_data)


def main():
    schema = "https://parsinger.ru/html/"
    base_url = "https://parsinger.ru/html/index4_page_1.html"
    dir_path = os.path.join(os.getcwd(), "data/csv_files")
    file_path = os.path.join(dir_path, "res.csv")
    hdd_table = parse_hdd_info(base_url, schema)
    list_to_csv(file_path, hdd_table)


if __name__ == "__main__":
    main()

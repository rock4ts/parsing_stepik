import csv
import os

import requests
from bs4 import BeautifulSoup


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


def parse_category_pages(page_urls: list, device_data: list) -> list:
    """
    Функция постраничного парсинга информации о девайсах определённой
    категории.
    Добавляет в аргумент device_data списки с информацией
    о каждом устройстве категории. Ничего не возвращает.

    Аргументы:
        :page_urls - список адресов страниц с витринами товаров определённой
        категории.
        :device_data - список списков информации о товарах магазина.
    """

    for url in page_urls:
        page_soup = get_soup(url)
        # формируем список наименований девайсов
        names = [
            name.text.strip() for name in
            page_soup.find_all("a", class_="name_item")
        ]
        # находим элементы с описанием девайса
        description_tags = page_soup.find_all("div", class_="description")
        # формируем список списков с информацией о всех девайсах на странице
        description_data = [
            [
                value.split(":")[1].strip() for value in
                item.text.split("\n") if value
            ] for item in description_tags
        ]
        # парсим список цен
        prices = [
            price.text.strip() for price in
            page_soup.find_all("p", class_="price")
        ]
        # склеиваем names, description_data и prices
        # и получаем список списков с информацией о каждом девайсе категории
        page_data = list(
            map(lambda x, y, z: [x, *y, z], names, description_data, prices)
        )
        # добавляем информацию о девайсах категории в общую таблицу
        for row in page_data:
            device_data.append(row)


def parse_all_pages(base_url, schema):
    """
    Функция постраничного парсинга информации о всех представленных в магазине
    девайсах. Возвращает список списков с информацией о каждом
    устройстве.

    Аргументы:
        :base_url - любой url страницы, содержащей навигационное меню
        с ссылками на витрину товаров определённой категории.
        :schema - базовая часть ссылки на страницу с витриной товаров.
    """

    device_data = []
    base_soup = get_soup(base_url)
    # находим элемент меню категорий и парсим ссылки на их первые страницы
    category_menu = base_soup.find("div", class_="nav_menu")
    category_urls = [
        f"{schema}{a_tag['href']}" for a_tag in category_menu.find_all("a")
    ]
    # запускаем цикл парсинга по категориям
    for category_url in category_urls:
        base_soup = get_soup(category_url)
        # находим элемент пагинации и создаём список ссылок страниц категории
        pagen_tag = base_soup.find("div", class_="pagen")
        page_urls = [
            f"{schema}{a_tag['href']}" for a_tag in pagen_tag.find_all("a")
        ]
        # запускаем функцию постраничного парсинга
        # товаров определённой категории
        parse_category_pages(page_urls, device_data)

    return device_data


def list_to_csv(file_path, device_data):
    """
    Функция сохранения табличных данных в виде списка списков в csv-файл.

    Аргументы:
        :file_path - адрес csv-файла, куда производится запись данных.
        :device_data - данные объекта 'iterable of rows' для записи в csv-файл.
    """
    with open(file_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(device_data)


def main():
    schema = "https://parsinger.ru/html/"
    base_url = "https://parsinger.ru/html/index1_page_1.html"
    dir_path = os.path.join(os.getcwd(), "data/csv_files")
    file_path = os.path.join(dir_path, "res2.csv")
    device_data = parse_all_pages(base_url, schema)
    list_to_csv(file_path, device_data)


if __name__ == "__main__":
    main()

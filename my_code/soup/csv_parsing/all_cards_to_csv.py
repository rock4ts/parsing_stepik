import csv
import os

import requests
from bs4 import BeautifulSoup


def get_soup(url):
    """
    Функция, создающая объект BeautifulSoup.

    Аргументы:
        :url - адреса запроса
    """
    response = requests.get(url=url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def parse_category_urls(base_url, schema):
    """
    Функция, собирающая ссылки на страницы с товарными витринами всех категории.

    Аргументы:
        :base_url - url страницы, содержащей навигационное меню с ссылками
        на витрины существующих на сайте товарных категорий;
        :schema - базовая часть ссылки на страницу с витриной.
    """
    category_urls = []
    base_soup = get_soup(base_url)
    # находим элемент меню категорий
    category_menu = base_soup.find("div", class_="nav_menu")
    # находим элементы с ссылками
    category_url_tags = category_menu.find_all("a")
    # извлекаем относительную ссылку, добавляем к базовой и сохраняем в список
    for url_tag in category_url_tags:
        category_urls.append(f"{schema}{url_tag['href']}")
    return category_urls


def parse_page_urls(category_url, schema):
    """
    Функция, собирающая ссылки на страницы с адресами товарных карточек
    определённой категории.

    Аргументы:
        :category_url - url страницы, содержащей меню пагинации витрин
                        текущей товарной категории;
        :schema - базовая часть ссылки на страницу с товарной витриной.
    """
    page_urls = []
    category_soup = get_soup(category_url)
    # находим элемент меню пагинации
    pagination_menu = category_soup.find("div", class_="pagen")
    # находим элементы с ссылками
    page_tags = pagination_menu.find_all("a")
    # извлекаем относительную ссылку, добавляем к базовой и сохраняем в список
    for url_tag in page_tags:
        page_urls.append(f"{schema}{url_tag['href']}")
    return page_urls


def parse_card_urls(page_url, schema):
    """
    Функция собирающая адреса товарных карточек на текущей странице.

    Аргументы:
        :page_url - url страницы, содержащей ссылки на товарные карточки;
        :schema - базовая часть ссылки на страницу с карточкой.
    """
    card_urls = []
    page_soup = get_soup(page_url)
    # находим все элементы с ссылками на карточки
    card_tags = page_soup.select(".sale_button a")
    # извлекаем относительную ссылку, добавляем к базовой и сохраняем в список
    for url_tag in card_tags:
        card_urls.append(f"{schema}{url_tag['href']}")
    return card_urls


def get_every_card_url(base_url, schema):
    """
    Функция собирающая с сайта магазина все ссылки на товарные карточки.

    Аргументы:
        :base_url - url страницы, содержащей ссылки на витрины
                    товарных категории;
        :schema - базовая часть ссылки на страницу с витриной или карточкой.
    """
    every_card_url = []
    every_page_url = []
    # парсим ссылки на страницы внутри категории
    category_urls = parse_category_urls(base_url, schema)
    # парсим ссылки на все страницы с витринами
    for category_url in category_urls:
        every_category_page_url = parse_page_urls(category_url, schema)
        for page_url in every_category_page_url:
            every_page_url.append(page_url)
    # парсим ссылки на все товарные карточки на сайте магазина
    for page_url in every_page_url:
        every_page_card_url = parse_card_urls(page_url, schema)
        for card_url in every_page_card_url:
            every_card_url.append(card_url)
    return every_card_url


def parse_card(card_url):
    """
    Функция парсинга информации из карточки товара.
    Сохраняет данные в список и возвращает его.

    Аргументы:
        : card_url - ссылка на страницу товарной карточки.
    """

    card_data = []
    card_soup = get_soup(card_url)
    # находим в "супе" раздел с информацией о товаре
    card_info = card_soup.find("div", class_="description")
    # находим и сохраняем "наименование", "артикул", "бренд", "модель"
    card_data.append(card_info.find("p", id="p_header").text.strip())
    card_data.append(
        card_info.find("p", class_="article").text.split(":")[1].strip())
    card_data.append(
        card_info.find("li", id="brand").text.split(":")[1].strip())
    card_data.append(
        card_info.find("li", id="model").text.split(":")[1].strip())
    # находим и сохраняем "наличие", "цена" и "старая цена"
    card_data.append(
        card_info.find("span", id="in_stock").text.split(":")[1].strip())
    card_data.append(card_info.find("span", id="price").text.strip())
    card_data.append(card_info.find("span", id="old_price").text.strip())
    # сохраняем ссылку на карточку с товаром
    card_data.append(card_url)
    return card_data


def cards_to_csv(file_path, head_names, card_urls, parse_card_method):
    """
    Функция записи информации из товарных карточек в csv-файл.

    Аргументы:
        :file_path - путь к csv-файлу, куда производится запись
                     информации из карточек;
        :head_names - список заголовков;
        :card_urls - список адресов карточек;
        :parse_card_method - функция парсинга карточки.
    """

    file = open(file_path, "w", encoding="utf-8-sig", newline="")
    writer = csv.writer(file, delimiter=";")
    writer.writerow(head_names)
    # парсим карточки и построчно записываем полученную информацию в файл
    for card_url in card_urls:
        card_info = parse_card_method(card_url)
        writer.writerow(card_info)
    file.close()


def main():
    head_names = [
        "Наименование", "Артикул", "Бренд", "Модель",
        "Наличие", "Цена", "Старая цена", "Ссылка на карточку с товаром"
    ]
    schema = "https://parsinger.ru/html/"
    base_url = "https://parsinger.ru/html/index1_page_1.html#1_1"
    dir_path = os.path.join(os.getcwd(), "data/csv_files")
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        pass
    file_path = os.path.join(dir_path, "device_data.csv")
    card_urls = get_every_card_url(base_url, schema)
    cards_to_csv(file_path, head_names, card_urls, parse_card)


if __name__ == "__main__":
    main()

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


def parse_card_links(base_url, schema):
    """
    Функция постраничного парсинга адресов карточек с товаром.

    Аргументы:
        :base_url - любой url страницы, содержащей список ссылок
        на страницы с витриной товаров.
        :schema - базовая часть ссылки на страницу с карточкой товара.
    """
    card_links = []
    base_soup = get_soup(base_url)
    # находим элемент пагинации и собираем ссылки в список
    pagen_tag = base_soup.find("div", class_="pagen")
    page_urls = [
        f"{schema}{a_tag['href']}" for a_tag in pagen_tag.find_all("a")
    ]
    # собираем ссылки на карточки с товарами
    for url in page_urls:
        page_soup = get_soup(url)
        page_card_links = [
            f"{schema}{a_tag['href']}" for a_tag in
            page_soup.select(".sale_button a")
        ]
        for card_link in page_card_links:
            card_links.append(card_link)
    return card_links


def parse_watch_card(card_link):
    """
    Функция парсинга информации карточки с часами.
    Сохраняет согласно порядку заголовков данные в список и возвращает его.

    Аргументы:
        : card_link - ссылка на страницу карточки с часами
    """

    card_data = []
    card_soup = get_soup(card_link)
    card_info = card_soup.find("div", class_="description")
    # добавляем значение графы "наименование"
    card_data.append(card_info.find("p", id="p_header").text.strip())
    # добавляем значение графы "артикул"
    card_data.append(
        card_info.find("p", class_="article").text.split(":")[1].strip()
    )
    descriptions = card_info.find("ul", id="description").find_all("li")
    # добавляем значения начиная с графы "бренд" и до "сайт производителя"
    for value in descriptions:
        card_data.append(value.text.split(":")[1].strip())
    # добавляем значение графы "наличие"
    card_data.append(card_info.find(id="in_stock").text.split(":")[1].strip())
    # добавляем значение графы "цена"
    card_data.append(card_info.find(id="price").text.strip())
    # добавляем значение графы "старая цена"
    card_data.append(card_info.find(id="old_price").text.strip())
    # добавляем ссылку на карточку с часами
    card_data.append(card_link)
    return card_data


def cards_to_csv(file_path, head_names, card_links, parse_card_method):
    """
    Функция построчной записи данных карточек в csv-файл.
    Функция имеет универсальный характер, то есть может создавать и записывать
    в csv-файл карточки любых категорий товаров - необходимо только указать
    список заголовков head_names и функцию парсинга карточки parse_card_method. 

    Аргументы:
        :file_path - путь к csv-файлу, куда производится запись
                     информации о товарах;
        :head_names - список заголовков описания товара;
        :card_links - список адресов карточек;
        :parse_card_method - функция парсинга карточки.
    """

    file = open(file_path, "w", encoding="utf-8-sig", newline="")
    writer = csv.writer(file, delimiter=";")
    writer.writerow(head_names)
    # парсим карточки и построчно записываем полученную информацию в файл
    for card_link in card_links:
        card_info = parse_card_method(card_link)
        writer.writerow(card_info)
    file.close()


def main():
    head_names = [
        "Наименование", "Артикул", "Бренд", "Модель",
        "Тип", "Технология экрана", "Материал корпуса",
        "Материал браслета", "Размер", "Сайт производителя",
        "Наличие", "Цена", "Старая цена", "Ссылка на карточку с товаром"
    ]
    schema = "https://parsinger.ru/html/"
    base_url = "https://parsinger.ru/html/index1_page_1.html#1_1"
    dir_path = os.path.join(os.getcwd(), "data/csv_files")
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        pass
    file_path = os.path.join(dir_path, "watch_data.csv")
    card_links = parse_card_links(base_url, schema)
    cards_to_csv(file_path, head_names, card_links, parse_watch_card)


if __name__ == "__main__":
    main()

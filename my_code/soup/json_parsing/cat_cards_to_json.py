import json
import os

import requests
from bs4 import BeautifulSoup


def get_soup(url):
    """Создаёт объект BeautifulSoup."""
    response = requests.get(url=url)
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "lxml")


def get_category_page_urls(category_url, schema):
    """Создаёт список ссылок на страницы внутри товарной категории."""
    page_urls = []
    category_soup = get_soup(category_url)
    pagination_menu = category_soup.find("div", class_="pagen")
    page_tags = pagination_menu.find_all("a")
    for url_tag in page_tags:
        page_urls.append(f"{schema}{url_tag.get('href')}")
    return page_urls


def get_page_card_urls(page_url, schema):
    """Парсит с текущей страницы ссылки на товарные карточки."""
    page_card_urls = []
    page_soup = get_soup(page_url)
    card_link_tags = page_soup.find_all("div", class_="sale_button")
    for url_tag in card_link_tags:
        page_card_urls.append(f"{schema}{url_tag.find('a').get('href')}")
    return page_card_urls


def get_category_card_urls(category_url, schema):
    """Парсит все ссылки на товарные карточки внутри категории."""
    category_card_urls = []
    page_urls = get_category_page_urls(category_url, schema)
    for page_url in page_urls:
        category_card_urls.extend(get_page_card_urls(page_url, schema))
    return category_card_urls


def get_description_head_names(card_url):
    """Собирает с товарной карточки названия заголовков раздела description."""
    card_soup = get_soup(card_url)
    description_list = card_soup.find("ul", id="description").find_all("li")
    description_head_names = [li.get("id") for li in description_list]
    return description_head_names


def create_description_dict(description_head_names, description_list):
    """Создаёт словарь из списка заголовков description и их значений."""
    description_dict = {}
    for head_name, value in zip(description_head_names, description_list):
        description_dict[head_name] = value
    return description_dict


def parse_card_info(card_url, schema, description_head_names):
    """Парсит информацию товарной карточки и сохраняет её в список."""
    card_soup = get_soup(card_url)
    card_info = []
    # category
    card_info.append(card_url.replace(schema, "").split("/")[0])
    # name
    card_info.append(card_soup.find("p", id="p_header").text.strip())
    # article
    card_info.append(
        card_soup.find("p", class_="article").text.split(":")[1].strip())

    description_list = [
        li.text.split(":")[1].strip() for li in
        card_soup.find("ul", id="description").find_all("li")]
    # description
    card_info.append(
        create_description_dict(description_head_names, description_list))
    # count
    card_info.append(
        card_soup.find("span", id="in_stock").text.split(":")[1].strip())
    # price
    card_info.append(card_soup.find("span", id="price").text.strip())
    # old price
    card_info.append(card_soup.find("span", id="old_price").text.strip())
    # link
    card_info.append(card_url)
    return card_info


def create_card_dict(head_names, card_info):
    """Создаёт словарь из списка заголовков описания товара и их значений."""
    card_dict = {}
    for head_name, value in zip(head_names, card_info):
        card_dict[head_name] = value
    return card_dict


def parse_category_cards(category_url, schema, head_names):
    """Парсим все карточки товарной категории."""
    category_card_list = []
    category_card_urls = get_category_card_urls(category_url, schema)
    description_head_names = get_description_head_names(
        category_card_urls[0]
    )
    for card_url in category_card_urls:
        card_info = parse_card_info(card_url, schema, description_head_names)
        category_card_list.append(create_card_dict(head_names, card_info))
    return category_card_list


def main():
    """
    Подготовка параметров, запуск парсинга
    и сохранение результатов в json-файл по заданному file_path.
    """
    dir_path = os.path.join(os.getcwd(), "data/json_files")
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        pass
    file_path = os.path.join(dir_path, "cat_cards.json")
    schema = "https://parsinger.ru/html/"
    category_url = "https://parsinger.ru/html/index1_page_1.html"
    head_names = [
        "category", "name", "article", "description",
        "count", "price", "old_price", "link"
    ]
    result_json = parse_category_cards(category_url, schema, head_names)
    print(len(result_json))
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(result_json, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()

import json
import os
from collections.abc import Iterable

import requests
from bs4 import BeautifulSoup


def flatten(elements):
    """Распаковывает вложенные iterable объекты."""
    flatten_condition = (
        lambda x: isinstance(x, Iterable) and not isinstance(x, (str, bytes))
    )
    for element in elements:
        if flatten_condition(element):
            yield from flatten(element)
        else:
            yield element


def get_soup(url):
    """Создаёт объект BeautifulSoup."""
    response = requests.get(url=url)
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "lxml")


def get_category_urls(base_url, schema):
    """Создаёт список ссылок на товарные категории."""
    category_urls = []
    base_soup = get_soup(base_url)
    nav_menu = base_soup.find("div", class_="nav_menu")
    category_tags = nav_menu.find_all("a")
    for url_tag in category_tags:
        category_urls.append(f"{schema}{url_tag.get('href')}")
    return category_urls


def get_category_pages_urls(category_url, schema):
    """Создаёт список ссылок на страницы внутри товарной категории."""
    page_urls = []
    category_soup = get_soup(category_url)
    pagination_menu = category_soup.find("div", class_="pagen")
    page_tags = pagination_menu.find_all("a")
    for url_tag in page_tags:
        page_urls.append(f"{schema}{url_tag.get('href')}")
    return page_urls


def parse_category_head_names(category_url):
    """Создаёт список заголовков товарных карточек внутри категории."""
    category_soup = get_soup(category_url)
    head_names = ["Наименование"]
    item = category_soup.find(
        "div", class_="item_card").find_all("div", class_="item")[0]
    description = item.find("div", class_="description").find_all("li")
    description_names = [li.text.split(":")[0].strip() for li in description]
    for element in description_names:
        head_names.append(element)
    head_names.append("Цена")
    return head_names


def parse_page_items(page_url):
    """
    Создаёт список элементов,
    представляющих характеристики товаров на странице.
    """
    page_soup = get_soup(page_url)
    items = page_soup.find(
        "div", class_="item_card").find_all(class_="item")
    names = [
        item.find("a", class_="name_item").text.strip() for item in items]
    descriptions = [
        [
            record.split(":")[1].strip() for record in
            item.find("div", class_="description").text.strip().split("\n")
        ] for item in items
    ]
    prices = [
        item.find("div", class_="price_box").text.strip() for item in items
    ]
    page_items_info = [
        list(flatten(item_info)) for item_info in
        zip(names, descriptions, prices)
    ]
    return page_items_info


def parse_category_items(category_pages_urls):
    """
    Создаёт список элементов,
    содержащих характеристики товаров определённой категории.
    """
    category_items = []
    for page_url in category_pages_urls:
        category_items.extend(parse_page_items(page_url))
    return category_items


def create_item_dict(head_names, item_info):
    """
    Создаёт словарь из списка заголовков и товарных характеристик.
    """
    item_dict = {}
    for head_name, value in zip(head_names, item_info):
        item_dict[head_name] = value
    return item_dict


def create_category_dict_list(category_url, category_items):
    """
    Создаёт список словарей,
    содержащих характеристики товаров определённой категории.
    """
    dict_list = []
    head_names = parse_category_head_names(category_url)
    for item_info in category_items:
        dict_list.append(
            create_item_dict(head_names, item_info))
    return dict_list


def combine_dict_lists(category_urls, schema):
    """
    Создаёт списки словарей,
    содержащих характеристики товаров определённой категориии,
    и объединяет их в единый список.
    """
    result_list = []
    for category_url in category_urls:
        category_pages_urls = get_category_pages_urls(category_url, schema)
        category_items = parse_category_items(category_pages_urls)
        result_list.extend(
            create_category_dict_list(category_url, category_items)
        )
    return result_list


def main():
    """
    Собирает ссылки на товарные категории,
    создаёт список словарей с информацией
    о всех представленных на сайте товарах
    и сохраняет его в json файл.
    """
    dir_path = os.path.join(os.getcwd(), "data/json_files")
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        pass
    file_path = os.path.join(dir_path, "all_items_info.json")
    schema = "https://parsinger.ru/html/"
    base_url = "https://parsinger.ru/html/index1_page_1.html"
    category_urls = get_category_urls(base_url, schema)
    result_list = combine_dict_lists(category_urls, schema)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(result_list, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()

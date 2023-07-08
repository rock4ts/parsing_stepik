import json
import os
from collections.abc import Iterable

import requests
from bs4 import BeautifulSoup


def get_soup(url):
    response = requests.get(url=url)
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "lxml")


def flatten(elements):
    element = None
    flatten_condition = (
        lambda x: isinstance(x, Iterable) and not isinstance(x, (str, bytes))
    )
    for element in elements:
        if flatten_condition(element):
            yield from flatten(element)
        else:
            yield element


def parse_page_urls(category_url, schema):
    page_urls = []
    category_soup = get_soup(category_url)
    pagination_menu = category_soup.find("div", class_="pagen")
    page_tags = pagination_menu.find_all("a")
    for url_tag in page_tags:
        page_urls.append(f"{schema}{url_tag['href']}")
    return page_urls


def parse_head_names(category_url):
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


def parse_items_info(page_urls):
    items_info = []
    for page_url in page_urls:
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
        items_info.extend(page_items_info)
    return items_info


def create_item_dict(head_names, item_info):
    item_dict = {}
    for head_name, value in zip(head_names, item_info):
        item_dict[head_name] = value
    return item_dict


def create_dict_list(head_names, items_info):
    dict_list = []
    for item_info in items_info:
        dict_list.append(
            create_item_dict(head_names, item_info))
    return dict_list


def main():
    dir_path = os.path.join(os.getcwd(), "data/json_files")
    try:
        os.mkdir(dir_path)
    except FileExistsError:
        pass
    file_path = os.path.join(dir_path, "category_items_info.json")
    schema = "https://parsinger.ru/html/"
    category_url = "https://parsinger.ru/html/index1_page_1.html"
    head_names = parse_head_names(category_url)
    category_page_urls = parse_page_urls(category_url, schema)
    items_info = parse_items_info(category_page_urls)
    dict_list = create_dict_list(head_names, items_info)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(dict_list, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()

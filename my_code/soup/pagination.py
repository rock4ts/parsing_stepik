import requests
from bs4 import BeautifulSoup

schema = "https://parsinger.ru/html/"
first_page_mouses = "https://parsinger.ru/html/index3_page_1.html"
session = requests.Session()
response = session.get(url=first_page_mouses)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")
first_pages_per_category = [
    f"{schema}{category_ref['href']}" for category_ref in
    soup.find(class_="nav_menu").find_all("a")
]
page_links_mouses = [
    f"{schema}{link['href']}" for link in
    soup.find(class_="pagen").find_all("a")
]
device_names = []

# for page_url in page_links_mouses:
#     page_response = session.get(url=page_url)
#     page_response.encoding = "utf-8"
#     page_soup = BeautifulSoup(page_response.text, "lxml")
#     device_names.append(
#         [
#             device.find("a", class_="name_item").text for device in
#             page_soup.find(class_="item_card").find_all(class_="img_box")
#         ]
#     )
#
# print(device_list)

# device_number_sum = 0
#
# for page_url in page_links_mouses:
#     page_response = session.get(url=page_url)
#     page_response.encoding = "utf-8"
#     page_soup = BeautifulSoup(page_response.text, 'lxml')
#     device_refs = [
#         a_tag["href"] for a_tag in
#         page_soup.find(class_="item_card").find_all("a", class_="name_item")
#     ]
#     for device_ref in device_refs:
#         device_url = f"{schema}{device_ref}"
#         device_response = session.get(url=device_url)
#         device_response.encoding = "utf-8"
#         device_soup = BeautifulSoup(device_response.text, "lxml")
#         device_number_sum += (
#             int(device_soup.find(
#                 "p", class_="article").text.split(":")[-1].strip())
#         )
#
# print(device_number_sum)

first_pages_per_category = [
    f"{schema}{category_ref['href']}" for category_ref in
    soup.find(class_="nav_menu").find_all("a")
]
page_urls_all = []

for category_first_page in first_pages_per_category:
    category_response = session.get(url=category_first_page)
    category_response.encoding = "utf-8"
    category_soup = BeautifulSoup(category_response.text, "lxml")
    [
        page_urls_all.append(f"{schema}{page_ref['href']}") for page_ref in
        category_soup.find(class_="pagen").find_all("a")
    ]

total_cost = 0

for page_url in page_urls_all:
    page_response = session.get(url=page_url)
    page_response.encoding = "utf-8"
    page_soup = BeautifulSoup(page_response.text, "lxml")
    device_urls = [
        f"{schema}{a_tag['href']}" for a_tag in
        page_soup.find(class_="item_card").find_all("a", class_="name_item")
    ]

    for device_url in device_urls:
        device_response = session.get(url=device_url)
        device_response.encoding = "utf-8"
        device_soup = BeautifulSoup(device_response.text, "lxml")
        devices_in_stock = (
            int(device_soup.find(id="in_stock").text.split(":")[-1])
        )
        price = (
            int(device_soup.find(id="price").text.split()[0])
        )
        total_cost += price * devices_in_stock

print(total_cost)

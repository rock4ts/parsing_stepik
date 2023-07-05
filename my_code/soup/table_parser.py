import requests

from bs4 import BeautifulSoup

# url = "https://parsinger.ru/table/1/index.html"
# response = requests.get(url=url)
# soup = BeautifulSoup(response.text, "lxml")
# rows = soup.find_all("tr")[1:]
# unique_nums = set()
# unique_sum = 0
# 
# for row in rows:
#     row_data = row.select("td")
#     for number in row_data:
#         unique_nums.add(float(number.text))
# 
# print(sum(unique_nums))

# url = "https://parsinger.ru/table/2/index.html"
# response = requests.get(url=url)
# soup = BeautifulSoup(response.text, "lxml")
# first_col_data = soup.select("td:nth-child(1)")
# first_column_sum = 0
# 
# for number in first_col_data:
#     first_column_sum += float(number.text)
# 
# print(first_column_sum)

# url = "https://parsinger.ru/table/3/index.html"
# response = requests.get(url=url)
# soup = BeautifulSoup(response.text, "lxml")
# numbers = soup.select("td>b")
# sum = sum([float(num.text) for num in numbers])
# print(sum)

# url = "https://parsinger.ru/table/4/index.html"
# response = requests.get(url=url)
# soup = BeautifulSoup(response.text, "lxml")
# green_numbers = soup.select("td.green")
# green_numbers_f_all = soup.find_all("td", class_="green")
# sum_green = sum([float(num.text) for num in green_numbers])
# sum_green_f_all = sum([float(num.text) for num in green_numbers_f_all])
# print(sum_green)
# print(sum_green_f_all)

# url = "https://parsinger.ru/table/5/index.html"
# response = requests.get(url=url)
# soup = BeautifulSoup(response.text, "lxml")
# rows = soup.find_all("tr")[1:]
# sum_products = 0
# 
# for row in rows:
#     orange = float(row.find(class_="orange").text)
#     blue = float(row.select("td:last-child")[-1].text)
#     sum_products += orange * blue
# 
# print(sum_products)

url = "https://parsinger.ru/table/5/index.html"
response = requests.get(url=url)
soup = BeautifulSoup(response.text, "lxml")
table_cols = soup.find_all("th")
table_rows = soup.find_all("tr")[1:]
col_sum_dict = {}

for i in range(0, len(table_cols)):
    sum_col = 0
    for row in table_rows:
        data = row.find_all("td")
        sum_col += float(data[i].text)
    table_col = table_cols[i].text
    col_sum_dict[table_col] = round(sum_col, 3)

print(col_sum_dict)

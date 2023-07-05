from pprint import pprint

import requests
from fake_useragent import UserAgent

ua = UserAgent()
headers = {
    'user-agent': ua.random,
    'x-requested-with': 'XMLHttpRequest'
}
# data = {
#     "GiveName": "Monero",
#     "GetName": "Dash",
#     "Sum": 100,
#     "Direction": 0
# }
# url = "https://bitality.cc/Home/GetSum"
url = "https://bitality.cc/hub/negotiate/"
response = requests.post(
    url=url, headers=headers, data={"negotiateVersion": 1})
pprint(response.json())

# url = "https://cbr.ru/cursonweek/"

# data_dollar = {
#     "DT": "",
#     "val_id": "R01235",
#     "_": "1667219511852"
# }
# data_euro = {
#     "DT": "",
#     "val_id": "R01239",
#     "_": "1667219511853"
# }

# response_dollar = requests.get(
#     url=url, headers=headers, params=data_dollar).json()[-1]
# response_euro = requests.get(
#     url=url, headers=headers, params=data_euro).json()[-1]

# print(response_dollar)
# print(response_euro)
# print(f"Дата: {response_dollar['data'][:10]}")
# print(f"Курс USD: {response_dollar['curs']} рублей")
# print(f"Курс EUR: {response_euro['curs']} рублей")

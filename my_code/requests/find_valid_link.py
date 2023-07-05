import requests
from http import HTTPStatus

url = 'https://parsinger.ru/task/1/'

for i in range(1, 501):
    link_url = f"{url}{i}.html"
    response = requests.get(link_url)
    if response.status_code == HTTPStatus.OK:
        print(link_url, response.text, sep='\n')
        break

# from random import choice
import time

import requests
from fake_useragent import UserAgent

name = "ip"
url = f"http://httpbin.org/{name}"
proxy = {
    'http': 'http://103.177.45.3:80',
    'https': 'http://103.177.45.3:80'
}
ua = UserAgent()

# with open('../user_agent.txt') as file:
#     lines = file.read().strip().split('\n')

for _ in range(3):
    fake_ua = {'user-agent': ua.random}
    response = requests.get(
        url=url,
        headers=fake_ua
    )
    print(response.text)
    time.sleep(5)

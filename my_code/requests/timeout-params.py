import requests
import time

url = 'http://httpbin.org/get'

proxies = {
    'http': 'http://200.12.55.90:80',
    'https': 'https://200.12.55.90:80'
}

start = time.perf_counter()
try:
    requests.get(url, proxies=proxies, timeout=1)
except Exception as err:
    print(time.perf_counter() - start)

params = {'key1': 'value1', 'key2': 'value2'}
response = requests.get(url, params=params)
print(response.text)
print(response.url)

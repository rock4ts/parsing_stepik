from random import choice
import requests

url = 'http://httpbin.org/ip'
good_proxies = '../data/good_proxies.txt'

with open(good_proxies) as file:
    proxy_file = file.read().split('\n')
    print(proxy_file)
    for elem in proxy_file:
        print(elem, sep='\n')
        try:
            ip = elem.strip()
            proxies = {
                'http': f'http//{ip}',
                'https': f'https//{ip}'
            }
            response = requests.get(url=url, proxies=proxies, timeout=15)
            print(response.json(), 'Successful connection')
        except Exception:
            continue

from random import choice
import requests

url = "http://httpbin.org/ip"
proxies_file_raw = '../data/proxy_list.txt'
good_proxies = '../data/good_proxies.txt'
num_proxies_req = 10

with open(proxies_file_raw) as raw, open(good_proxies, 'w') as good_proxies:
    raw_proxy_list = raw.read().split('\n')
    while num_proxies_req > 0 and raw_proxy_list:
        proxy = raw_proxy_list.pop(
            raw_proxy_list.index(choice(raw_proxy_list))).strip()
        proxies = {
            'http': f"http://{proxy}",
            'https': f"https://{proxy}"
        }
        try:
            response = requests.get(url, proxies=proxies, timeout=15)
            if response.status_code == 200:
                good_proxies.write(f"{proxy}\n")
                print(f"Найден рабочий прокси: {proxy}")
                num_proxies_req -= 1
        except Exception:
            continue

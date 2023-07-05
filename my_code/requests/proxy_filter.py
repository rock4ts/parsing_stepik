import requests

url = "http://httpbin.org/ip"
raw_proxies_txt = "../data/proxy_list.txt"
checked_proxies_txt = "../data/checked_proxies.txt"

with open(raw_proxies_txt) as raw, open(checked_proxies_txt, 'w') as g_proxies:
    raw_list = raw.read().split('\n')
    checked_list = []
    for i in range(0, len(raw_list), 10):
        ip = raw_list[i].strip()
        proxies = {
            'http': f"http://{ip}",
            'https': f"https://{ip}"
        }
        try:
            response = requests.get(url=url, proxies=proxies, timeout=10)
            if response.status_code == 200:
                g_proxies.write(f"{ip}\n")
                print(f"Найден рабочий прокси: {ip}")
        except:
            continue

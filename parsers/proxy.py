import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.gen_link = []
        self.completed_proxy_list = []
        self.pagen_count = 1
        self.user_agent = UserAgent()

    def gen_links_lst(self):  # генерирует список ссылок по заданому оффсету
        for offset in range(0, 3201, 64):  # 3201
            if offset == 0:
                link = 'https://hidemy.name/ru/proxy-list/#list'
            else:
                link = f'https://hidemy.name/ru/proxy-list/?start={offset}#list'
            self.gen_link.append(link)

    def get_html(self):  # получает хтмл с каждой страницы
        page = 0
        try:
            for link in self.gen_link:
                page += 1
                headers = {
                    'user-agent': self.user_agent.random,
                    'accept': '* / *'
                }
                response = requests.get(url=link, headers=headers)
                print(link)
                soup = BeautifulSoup(response.text, 'lxml')
                ip = soup.find('tbody').find_all('tr')
                port = soup.find('tbody').find_all('tr')
                for ip, port in zip(ip, port):
                    self.completed_proxy_list.append(
                        f"{ip.find_all('td')[0].text}:{port.find_all('td')[1].text} \n")
                print(f'page:{page}, proxies found:{len(self.completed_proxy_list)}')
        except Exception as _ex:
            print(_ex)

    def save_proxy_in_txt(self):    # записывает результат в файл
        with open('../data/proxy_list.txt', 'w') as file:
            for proxy in self.completed_proxy_list:
                file.write(proxy)

    def main(self):
        self.gen_links_lst()
        parse.get_html()
        self.save_proxy_in_txt()


if __name__ == '__main__':
    parse = Parser()
    parse.main()

import requests
import lxml
from bs4 import BeautifulSoup


url = 'http://foxtools.ru/Proxy?al=False&am=False&ah=True&ahs=True&http=True&https=False'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
}

def get_valid_proxy_url(url, headers):
    # получение списка действующих прокси
    # парсинг страницы
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    tags = soup.find_all(attrs={'onclick':'SelectProxy(this)'})
    # получение списка прокси и проверка их
    tags_count = 10 if len(tags) >=  10 else len(tags)
    proxy_url_raw = [tags[i]['value'] for i in range(tags_count)]
    proxy_url_valid = []
    for url in proxy_url_raw:
        try:
            r = requests.get(url='http://' + url, headers=headers)
            r.raise_for_status
            proxy_url_valid.append(url)
        except requests.exceptions.RequestException:
            continue
    return proxy_url_valid

get_valid_proxy_url(url, headers)
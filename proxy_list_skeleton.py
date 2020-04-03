'''
Модуль ищет на заданном сайте действующий прокси, и передает его по требованию.
Список действующих прокси НЕ самообновляется, так как использованные прокси пришлось бы
записывать в файл, а heroku не поддерживает создание и чтение из файла.
В случае невозможности получить новый действующий прокси, отправится смс об этом на телефон
'''

# !!!! рабочий вариант
# Получает список всех прокси с сайта без проверки на валидность.

import requests
import lxml
from bs4 import BeautifulSoup


url = 'http://foxtools.ru/Proxy?al=False&am=False&ah=True&ahs=True&http=True&https=False'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
}

def get_raw_proxy_list():
    # получение списка прокси
    # на данном этапе валидность прокси не проверяется, только уникальность
    # парсинг страницы
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    tags = soup.find_all(attrs={'onclick':'SelectProxy(this)'})
    # получение списка прокси 
    raw_proxy_list = [tags[i]['value'] for i in range(len(tags))]
    print(raw_proxy_list)
    return raw_proxy_list

raw_proxy_list = get_raw_proxy_list()
    
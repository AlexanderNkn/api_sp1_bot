'''
Модуль ищет на заданном сайте действующий прокси, и передает его по требованию.
Список действующих прокси самообновляется.
В случае невозможности получить новый действующий прокси, отправится смс об этом на телефон
'''
# !!! рабочий вариант, выдает по 1 валидированному прокси за запрос. Нужно доработать.

# !!!! в этом модуле есть код, который сравнивает урл с уже использаванными.
# списки использованных урлов храняться в оперативной памяти, соответственно при
# перезапуске питона, списки использованных урлов пропадают. Надо сбрасывать использованные
# в текстовый файл и оттуда подгружать. На хероку нет функционала по созданию, редактированию
# текстового файла. Поэтому пока этот модуль приостановлен. Работа продолжается в 
# proxy_simple.py, без проверки на использованные урлы.

import requests
import lxml
from bs4 import BeautifulSoup


url = 'http://foxtools.ru/Proxy?al=False&am=False&ah=True&ahs=True&http=True&https=False'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
}

def get_raw_proxy_list(proxy_list_old=[]):
    # получение списка прокси, пока не использовавшихся в работе
    # на данном этапе валидность прокси не проверяется, только уникальность
    # парсинг страницы
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    tags = soup.find_all(attrs={'onclick':'SelectProxy(this)'})
    # получение списка прокси и сверка их со старым списком
    count_new = 0   #счетчик количества новых прокси (создаем лист из 5)
    count_all = -1   #счетчик прокси перебранных на сайте
    proxy_list_raw_new = []
    while count_new < 5:
        count_all += 1
        if tags[count_all]['value'] not in proxy_list_old: # проверяем, не использовался ли уже этот прокси
            proxy_list_raw_new.append(tags[count_all]['value']) # создаем список из новых прокси
            count_new += 1
    proxy_list_old += proxy_list_raw_new #формируем список когда-либо использовавшихся прокси
#    print(proxy_list_old, proxy_list_raw_new)
    return proxy_list_old, proxy_list_raw_new
    
    
# def get_valid_proxy_url(proxy_url_raw_new):
#     # из списка
#     proxy_url_valid = []
#     for url in proxy_url_raw_new:
#         try:
#             r = requests.get(url='http://' + url, headers=headers)
#             r.raise_for_status
#             proxy_url_valid.append(url)
#         except requests.exceptions.RequestException:
#             continue
#     print(proxy_url_valid)
#     return proxy_url_valid

# proxy_url_old, proxy_url_raw_new = get_raw_proxy_url(url, headers, proxy_url_old=proxy_url_old)
# proxy_url = get_valid_proxy_url(proxy_url_raw_new)

def get_valid_proxy_url(proxy_list_raw_new, used_url=[]):
    while True:
        count_invalid = 0   # счетчик нерабочих прокси
        for url in proxy_list_raw_new:
            if url not in used_url:
                try:
                    r = requests.get(url='http://' + url, headers=headers)
                    r.raise_for_status
                    return url
                except requests.exceptions.RequestException:
                    count_invalid += 1
                    # если в списке все прокси нерабочие, перенаправляем за новым списком
                    if count_invalid == len(proxy_list_raw_new):
                        get_raw_proxy_list(url, headers, proxy_list_old=[])
                        break
                    continue
            else:
                count_invalid += 1
                # если в списке все прокси нерабочие, перенаправляем за новым списком
                if count_invalid == len(proxy_list_raw_new):
                    proxy_list_raw_new = get_raw_proxy_list(proxy_list_old=proxy_list_old)[1]
                    break
                continue


proxy_list_old, proxy_list_raw_new = get_raw_proxy_list()

def get_proxy(used_url=[]):
    valid_url = get_valid_proxy_url(proxy_list_raw_new, used_url)
    if valid_url not in used_url:
        used_url.append(valid_url)
        print(valid_url)
        return used_url

used_url = get_proxy()

get_proxy(used_url)
get_proxy(used_url)
get_proxy(used_url)
get_proxy(used_url)
get_proxy(used_url)
get_proxy(used_url)
get_proxy(used_url)
get_proxy(used_url)
get_proxy(used_url)
get_proxy(used_url)
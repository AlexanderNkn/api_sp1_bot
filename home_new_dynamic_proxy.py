# начал совмещать основного бота с модулем получения списка прокси. Но выяснил,
# что нет нормальных сайтов с валидными прокси. Из-за этого посыпались ошибки от 
# бота телеграмма. Пока приостановил, жду нормального списка для продолжения работы.

import json
import os
import time

import lxml
import requests
import telegram
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
PROXY_SITE_URL = os.getenv('PROXY_SITE_URL')
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    }

def get_raw_proxy_list():
    # получение списка прокси
    # на данном этапе валидность прокси не проверяется, только уникальность
    # парсинг страницы
    r = requests.get(url=PROXY_SITE_URL, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    tags = soup.find_all(attrs={'onclick':'SelectProxy(this)'})
    # получение списка прокси 
    raw_proxy_list = [tags[i]['value'] for i in range(len(tags))]
    print(raw_proxy_list)
    return raw_proxy_list

raw_proxy_list = get_raw_proxy_list()

def get_valid_proxy_url(raw_proxy_list):
    for url in raw_proxy_list:
        try:
            url = 'http://' + url
            r = requests.get(url, headers=headers)
            r.raise_for_status
            return url
        except requests.exceptions.RequestException:
            continue

proxy_url=get_valid_proxy_url(raw_proxy_list)

proxy = telegram.utils.request.Request(proxy_url=proxy_url)
bot = telegram.Bot(token=TELEGRAM_TOKEN, request='http://31.45.243.11:80')

def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    if homework.get('status') == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    params = {'from_date': current_timestamp}
    while True:
        try:
            homework_statuses = requests.get(
                'https://praktikum.yandex.ru/api/user_api/homework_statuses/',
                headers=headers, 
                params=params
            )
            homework_statuses.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f'Сервер яндекса упал с ошибкой: {e}')
        else:
            try:
                return homework_statuses.json()
            except json.JSONDecodeError:
                print(f'Сервер отвечает, но в возвращаемой с сайта странице нет json')
        time.sleep(5)


def send_message(message):
    return bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    current_timestamp = 0  # начальное значение timestamp
    
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks', [],):
                send_message(parse_homework_status(new_homework.get('homeworks')[0]))
            current_timestamp = new_homework.get('current_date')  # обновить timestamp
            time.sleep(1200)  # опрашивать раз в 20 минут

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}; имя ошибки: {e.__class__.__name__}')
            time.sleep(5)


if __name__ == '__main__':
    main()

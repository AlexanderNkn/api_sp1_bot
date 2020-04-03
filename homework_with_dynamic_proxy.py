# начал совмещать основного бота с модулем получения списка прокси. Но выяснил,
# что нет нормальных сайтов с валидными прокси. Из-за этого посыпались ошибки от 
# бота телеграмма. Пока приостановил, жду нормального списка для продолжения работы.

import json
import os
import time

import requests
import telegram
from telegram.error import TimedOut, NetworkError
from dotenv import load_dotenv

from proxy import get_raw_proxy_list


load_dotenv()

PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
NEED_PROXY = os.getenv('need_proxy')


def get_telegram_bot(used_url, raw_proxy_list):
    if used_url:
        print(f'URL {used_url} больше не работает')
    if used_url in raw_proxy_list:
        raw_proxy_list.remove(used_url)
        print(f'Осталось {len(raw_proxy_list)} прокси')
        if len(raw_proxy_list) == 0:
            raw_proxy_list = get_raw_proxy_list()
    if len(raw_proxy_list) == 25:
        print('Получен новый список прокси')
    for url in raw_proxy_list:
        proxy_url = 'socks5://' + url
        print(f'новый {proxy_url}')
        proxy = telegram.utils.request.Request(proxy_url=proxy_url)
        bot = telegram.Bot(token=TELEGRAM_TOKEN, request=proxy or None)
        return bot, url, raw_proxy_list


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
    raw_proxy_list = get_raw_proxy_list()
    bot, url, raw_proxy_list = get_telegram_bot(used_url=None, raw_proxy_list=raw_proxy_list)
    while True:
        try:
            return bot.send_message(chat_id=CHAT_ID, text=message)
        except (TimedOut, NetworkError):
            used_url = url
            bot, url, raw_proxy_list = get_telegram_bot(used_url, raw_proxy_list)
            continue


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

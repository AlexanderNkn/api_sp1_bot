import json
import os
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
PROXY_URL = os.getenv('proxy_url')

proxy = telegram.utils.request.Request(proxy_url=PROXY_URL)
bot = telegram.Bot(token=TELEGRAM_TOKEN, request=proxy)

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

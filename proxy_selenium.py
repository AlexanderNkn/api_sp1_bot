'''
Эта версия proxy.py для размещения на selenium.
Модуль ищет на сайте http://spys.one/socks/ прокси и выгружает их в список. 
Можно использовать на страницах с javascript, так как для парсинга используется selenium.
При использовании lxml и BeautifulSoup4 порты у адресов прокси с этого сайта 
отображались в зашифрованном виде.
'''
import os

from selenium import webdriver

from twilio_sms import \
    sms_sender  # импортируем функцию отправки сообщений через твилио

CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

options = webdriver.ChromeOptions()
options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--headless')

def parse_proxy_site():
    '''
    Получаем список прокси с сайта без проверки на валидность
    '''
    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH, 
        chrome_options=options
    )
    driver.get('http://spys.one/socks/')
    # класс, в котором находятся прокси, называется 'spy14' 
    content = driver.find_elements_by_class_name('spy14')
    # получаем список текстовых данных, в которых кроме прокси содержится другая информация, 
    # так как класс 'spy14' содержит еще и другие данные(например названия городов, стран)
    content_list = [item.text for item in content]
    # вырезаем из текстовых данных прокси
    url_list = []
    for item in content_list:
        for i in item:
            # можно(нужно?) переделать через регулярные выражения
            if i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,':'] and len(item) > 5:
                url_list.append(item)
    driver.close()
    return url_list

def get_raw_proxy_list():
    '''
    забирает список прокси, а в случае невозможности, запускает отправку
    сообщения об ошибке.
    '''
    try:
        url_list = parse_proxy_site()
        if not url_list:
            sms_sender('Список прокси для телеграмм бота устарел. Сайт с прокси не отвечает.')
        return url_list
    except Exception as e:
        sms_sender(f'Модуль proxy_selenium упал с ошибкой: {e}')
        return []

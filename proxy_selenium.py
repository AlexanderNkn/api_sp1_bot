'''
Эта версия proxy.py для размещения на selenium.
Модуль ищет на сайте http://spys.one/socks/ прокси и выгружает их в список. 
!!! Можно использовать на страницах с javascript, так как для парсинга используется selenium.
При использовании lxml и BeautifulSoup4 порты у адресов прокси с этого сайта 
отображались в зашифрованном виде.
'''

from selenium import webdriver

from twilio_sms import sms_sender # импортируем функцию отправки сообщений через твилио


GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = GOOGLE_CHROME_BIN

def parse_proxy_site():
    '''
    Получаем список прокси с сайта без проверки на валидность
    '''
    browser = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH, 
        chrome_options=chrome_options
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
    '''забирает список прокси, а в случае невозможности, запускает отправку
    сообщения об ошибке'''
    url_list = parse_proxy_site()
    if not url_list:
        sms_sender('Список прокси для телеграмм бота устарел. Сайт с прокси не отвечает.')
    return url_list

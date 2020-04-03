'''
Модуль ищет и выгружает с сайта прокси. 
!!! Можно использовать на страницах с javascript
Как в данном случае - порты на http://spys.one/socks/ отображались 
в зашифрованном виде.
'''

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()

def get_raw_proxy_list():
    '''
    Получаем список прокси с сайта без проверки на валидность
    '''
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(
        '/usr/local/bin/chromedriver', 
        chrome_options = chrome_options
    )
    driver.get('http://spys.one/socks/')
    # класс, в котором находятся прокси, называется 'spy14' 
    content = driver.find_elements_by_class_name('spy14')
    # получаем список текстовых данных, в которых кроме прокси содержится другая информация, 
    # так как класс 'spy14' содержит еще и другие данные
    content_list = [item.text for item in content]
    # получаем из текстовых данных только прокси
    url_list = []
    for item in content_list:
        for i in item:
            if i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,':'] and len(item) > 5:
                url_list.append(item)
    print(url_list)
    driver.close()
    return url_list

raw_proxy_list = get_raw_proxy_list()


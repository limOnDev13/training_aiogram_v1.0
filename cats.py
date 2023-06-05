import requests
import time


API_URL: str = 'https://api.telegram.org/bot'
API_CATS_URL: str = 'https://api.thecatapi.com/v1/images/search'
BOT_TOKEN: str = '6062355303:AAGWf8Pseg9XloZDpiA0PmMsxmhNi7orb5w'
ERROR_TEXT: str = 'Ошибка! Здесь должны быть котики...'
MAX_COUNTER: int = 100

offset: int = -2
counter: int = 0
cat_response: requests.Response
cat_link: str


while counter < MAX_COUNTER:
    print(f'Попытка номер {counter}')

    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset='
                           f'{offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            cat_response = requests.get(API_CATS_URL)
            if cat_response.status_code == 200:
                cat_link = cat_response.json()[0]['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id='
                             f'{chat_id}&text={ERROR_TEXT}')

            counter += 1
            time.sleep(1)

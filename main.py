import requests
import time
import add_functions


API_URL: str = 'https://api.telegram.org/bot'  # По сути своей
# таким образом можно обращаться к любому открытому API,
# необязательно к телеге
# не выкладывать токен на Гит!!!!!!!!
BOT_TOKEN: str = add_functions.read_token_from_txt()
# Это сообщение будет выводиться при каждом апдейте.
TEXT: str = 'Чувак, вот тебе сообщение...'
# Максимальное число апдейтов
MAX_COUNTER: int = 20

# offset - сдвиг. Этот параметр необходим для GET запроса getUpdates
# Если использовать getUpdates без параметра offset (или offset=0),
# то на сервак будут приходить все апдейты за последние 24 часа при
# каждом вызове метода. Если использовать номер последнего апдейта + 1,
# то сервер будет отправлять нам только те апдейты, которые идут за
# последним, полученным до очередного запроса апдейтов.
# Если установить offset=-1, то сервер передаст последний апдейт.
offset: int = -2
counter: int = 0
chat_id: int

# Все это счастье будет крутиться в бесконечном цикле событий.
while counter < MAX_COUNTER:
    print(f'Попытка номер {counter}')

    # Получаем последний апдейт. При старте offset уйдет со значением -1
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset='
                           f'{offset + 1}').json()

    # Если результат не пустой, отправим сообщение и изменим offset
    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id='
                         f'{chat_id}&text={TEXT}')

            counter += 1

    # Необходимо делать паузы, чтобы постоянные запросы
    # в бесконечном цикле не свернули башку серваку.
    time.sleep(1)

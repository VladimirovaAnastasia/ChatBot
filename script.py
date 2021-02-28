import logging
import time

import requests
import os
from dotenv import load_dotenv
import telegram

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format="%(asctime)s - [%(levelname)s] - %(message)s",
)
payload = None


def get_data(headers, url):
    try:
        global payload
        print('1')
        response = requests.get(url, headers=headers, params=payload)
        data = response.json()
        print(data)
        if data['status'] == 'found':
            result = data['new_attempts'][0]
            send_message(result['is_negative'], result['lesson_title'])
            timestamp = result['timestamp']
        else:
            timestamp = data['timestamp_to_request']
        payload = {"timestamp": timestamp}
    except requests.exceptions.ReadTimeout:
        logging.error('Read Timeout')
        time.sleep(5)
    except requests.exceptions.ConnectionError:
        logging.error('Connection Error')
        time.sleep(5)


def send_message(is_negative, lesson_title):
    TG_TOKEN = os.getenv("TG_TOKEN")
    TG_CHAT_ID = os.getenv("TG_CHAT_ID")
    HTTP_PROXY = os.getenv('HTTP_PROXY')
    pp = telegram.utils.request.Request(proxy_url=HTTP_PROXY)
    bot = telegram.Bot(token=TG_TOKEN, request=pp)

    message = f'У вас проверили работу "{lesson_title}"' + '\n\n'
    if is_negative:
        message = message + 'К сожалению, в работе нашлись ошибки.'
    else:
        message = message + 'Предователю все понравилось, можно приступать к следующему уроку!'

    bot.send_message(chat_id=TG_CHAT_ID, text=message)


def main():
    DEVMAN_API_TOKEN = os.getenv("DEVMAN_API_TOKEN")
    headers = {
        "Authorization": f'Token {DEVMAN_API_TOKEN}'
    }
    url = 'https://dvmn.org/api/long_polling/'

    while True:
        get_data(headers, url)


if __name__ == '__main__':
    main()

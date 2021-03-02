import logging
import time

import requests
import os
from dotenv import load_dotenv
import telegram

logger = logging.getLogger()


def check_work_status(headers, url):
    payload = None

    while True:
        try:
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            data = response.json()

            if data['status'] == 'found':
                result = data['new_attempts'][0]
                send_message(result['is_negative'], result['lesson_title'])
                timestamp = result['timestamp']
            else:
                timestamp = data['timestamp_to_request']

            payload = {"timestamp": timestamp}
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            logger.exception('Connection Error')
            time.sleep(5)
        except requests.exceptions.HTTPError:
            logger.exception('HTTPError')


def send_message(is_negative, lesson_title):
    tg_token = os.getenv("TG_TOKEN")
    tg_chat_id = os.getenv("TG_CHAT_ID")
    http_proxy = os.getenv('HTTP_PROXY')

    pp = telegram.utils.request.Request(proxy_url=http_proxy)
    bot = telegram.Bot(token=tg_token, request=pp)

    message = f'У вас проверили работу "{lesson_title}"' + '\n\n'
    if is_negative:
        message = message + 'К сожалению, в работе нашлись ошибки.'
    else:
        message = message + 'Предователю все понравилось, можно приступать к следующему уроку!'

    bot.send_message(chat_id=tg_chat_id, text=message)


def main():
    logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S', format="%(asctime)s - [%(levelname)s] - %(message)s")
    logger.setLevel(logging.INFO)

    load_dotenv()
    devman_api_token = os.getenv("DEVMAN_API_TOKEN")

    headers = {
        "Authorization": f'Token {devman_api_token}'
    }
    url = 'https://dvmn.org/api/long_polling/'

    check_work_status(headers, url)


if __name__ == '__main__':
    main()

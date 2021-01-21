import requests
import telegram
from dotenv import load_dotenv
import os
from time import sleep
from pprint import pprint


def get_check_result(url, tg_token, chat_id):
    timestamp = None
    while True:
        headers = {'Authorization': 'Token 3dabacd9bf959a599899d9bc8515081c471c4eb0'}
        params = {'timestamp': timestamp}
        response = requests.get(url, headers=headers, params=params, timeout=95)
        response.raise_for_status()
        bot = telegram.Bot(token=tg_token)
        lesson_result = response.json()
        if lesson_result['status'] == 'found':
            new_attempt = lesson_result['new_attempts'][0]
            lesson_title = new_attempt['lesson_title']
            lesson_url = new_attempt['lesson_url']
            negative_result = new_attempt['is_negative']
            timestamp = lesson_result['last_attempt_timestamp']
            if negative_result:
                bot.send_message(chat_id=chat_id,
                                 text='''У вас проверили работу - {} https://dvmn.org{}. Есть ошибки!'''.format(lesson_title, lesson_url))
            else:
                bot.send_message(chat_id=chat_id,
                                 text='У вас проверили работу - {} https://dvmn.org{}. Работу приняли!'.format(lesson_title, lesson_url))
        elif lesson_result['status'] == 'timeout':
            timestamp = lesson_result['timestamp_to_request']


if __name__ == '__main__':
    load_dotenv()
    os.environ['DEVMAN_TOKEN']
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    tg_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    devman_token = os.getenv('DEVMAN_TOKEN')
    url_long_polling = 'https://dvmn.org/api/long_polling/'
    while True:
        try:
            get_check_result(url_long_polling, devman_token, tg_bot_token, chat_id)
        except requests.exceptions.ReadTimeout:
            print('error ReadTimeout')
        except requests.exceptions.ConnectionError:
            print('error ConnectionError')
            sleep(5)

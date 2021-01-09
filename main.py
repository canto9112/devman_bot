import requests
import telegram
from dotenv import load_dotenv
import os


def get_timestamp_to_request(url, dvm_token, tg_token, chat_id):
    timestamp = None
    while True:
        headers = {'Authorization': dvm_token}
        params = {'timestamp': timestamp}
        response = requests.get(url, headers=headers, params=params, timeout=95)
        response.raise_for_status()
        bot = telegram.Bot(token=tg_token)
        if response.json()['status'] == 'found':
            lesson_title = response.json()['new_attempts'][0]['lesson_title']
            lesson_url = response.json()['new_attempts'][0]['lesson_url']
            negative_result = response.json()['new_attempts'][0]['is_negative']
            timestamp = response.json()['last_attempt_timestamp']
            if negative_result:
                bot.send_message(chat_id=chat_id, text='У вас проверили работу - {}\n'
                                                       'https://dvmn.org{}\n'
                                                       'Есть ошибки!'.format(lesson_title, lesson_url))
            else:
                bot.send_message(chat_id=chat_id, text='У вас проверили работу - {}\n'
                                                       'https://dvmn.org{}\n'
                                                       'Работу приняли!'.format(lesson_title, lesson_url))
        elif response.json()['status'] == 'timeout':
            timestamp = response.json()['timestamp_to_request']


if __name__ == '__main__':
    load_dotenv()
    chat_id = os.getenv('chat_id')
    tg_bot_token = os.getenv('tg_bot_token')
    devman_token = os.getenv('devman_token')
    url_long_polling = 'https://dvmn.org/api/long_polling/'
    while True:
        try:
            get_timestamp_to_request(url_long_polling, devman_token, tg_bot_token, chat_id)
        except requests.exceptions.ReadTimeout:
            print('error ReadTimeout')
        except requests.exceptions.ConnectionError:
            print('error ConnectionError')

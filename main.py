import requests
from pprint import pprint
import telegram

def user_reviews(token, url):
    headers = {
        'Authorization': token
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    user_reviews = response.json()
    pprint(user_reviews)
    return user_reviews['results'][0]['timestamp']


def get_timestamp_to_request(url, dvm_token, tg_token, chat_id):
    while True:
        headers = {'Authorization': dvm_token}
        response = requests.get(url, headers=headers, timeout=95)
        response.raise_for_status()

        if response.json()['status'] == 'found':
            pprint(response.json())

            bot = telegram.Bot(token=tg_token)
            bot.send_message(chat_id=chat_id, text='Работа проверена')
            timestamp = response.json()['last_attempt_timestamp']
            print(timestamp)

        elif response.json()['status'] == 'timeout':
            timestamp = response.json()['timestamp_to_request']
            print(timestamp)


if __name__ == '__main__':
    chat_id = 335031317
    tg_bot_token = '1505719734:AAF6FBmh5090CiuWUq2KWO_wUC-mH__A8kM'
    devman_token = 'Token 3dabacd9bf959a599899d9bc8515081c471c4eb0'
    URL_CHECKS_WORKS = 'https://dvmn.org/api/user_reviews/'
    URL_LONG_POLLING = 'https://dvmn.org/api/long_polling/'
    while True:
        try:
            get_timestamp_to_request(URL_LONG_POLLING, devman_token, tg_bot_token, chat_id)
        except requests.exceptions.ReadTimeout:
            print('error ReadTimeout')
        except requests.exceptions.ConnectionError:
            print('error ConnectionError')
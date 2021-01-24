import requests
import telegram
from dotenv import load_dotenv
import os
from logger_bot import MyLogsHandler
from time import sleep
import logging


telegram_logger = logging.getLogger('bot')


def get_check_result(url, chat_id, devman_token):
    timestamp = None
    while True:
        headers = {'Authorization': f'Token {devman_token}'}
        params = {'timestamp': timestamp}
        response = requests.get(url, headers=headers, params=params, timeout=95)
        response.raise_for_status()
        lesson_result = response.json()
        if lesson_result['status'] == 'found':
            new_attempt = lesson_result['new_attempts'][0]
            lesson_title = new_attempt['lesson_title']
            lesson_url = new_attempt['lesson_url']
            negative_result = new_attempt['is_negative']
            timestamp = lesson_result['last_attempt_timestamp']
            if negative_result:
                bot.send_message(
                    chat_id=chat_id,
                    text=f'У вас проверили работу - {lesson_title} https://dvmn.org{lesson_url}. Есть ошибки!')
            else:
                bot.send_message(
                    chat_id=chat_id,
                    text=f'У вас проверили работу - {lesson_title} https://dvmn.org{lesson_url}. Работу приняли!')
        elif lesson_result['status'] == 'timeout':
            timestamp = lesson_result['timestamp_to_request']


if __name__ == '__main__':
    load_dotenv()
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    tg_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    devman_token = os.getenv('DEVMAN_TOKEN')
    url_long_polling = 'https://dvmn.org/api/long_polling/'

    logging.getLogger('dotenv').setLevel('CRITICAL')
    logging.getLogger('telegram').setLevel('CRITICAL')
    logging.getLogger('urllib3').setLevel('CRITICAL')

    bot = telegram.Bot(token=tg_bot_token)

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s  %(levelname)s %(message)s')
    telegram_logger.addHandler(MyLogsHandler(bot, chat_id))
    telegram_logger.debug('Старт бота')

    while True:
        try:
            get_check_result(url_long_polling, chat_id, devman_token)
        except requests.exceptions.ReadTimeout:
            telegram_logger.error('Бот упал с ошибкой - ReadTimeout')
        except requests.exceptions.ConnectionError:
            telegram_logger.error('Бот упал с ошибкой - ConnectionError')
            sleep(60)



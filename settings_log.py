import logging
import telegram


def push_log_telegtam(tg_bot_token, chat_id):
    bot = telegram.Bot(token=tg_bot_token)
    class MyLogsHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            bot.send_message(chat_id=chat_id, text=log_entry)


    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s  %(levelname)s %(message)s')
    logger = logging.getLogger('BOT')
    logger.addHandler(MyLogsHandler())
    return logger
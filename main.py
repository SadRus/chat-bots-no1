import argparse
import logging
import os
import requests
import telegram

from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from time import time


class TelegramLogsHandler(RotatingFileHandler):

    def __init__(self, filename, tg_bot, chat_id, **kwargs):
        super().__init__(filename, **kwargs)
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        super().emit(record)
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def create_logger(tg_bot, chat_id, dest_folder, max_bytes=200, backup_count=2):
    logs_full_path = os.path.join(dest_folder, 'bot.log')
    logging.basicConfig(
        level=logging.INFO,
        filename=logs_full_path,
        filemode='w',
        format="%(asctime)s %(process)s %(levelname)s %(message)s",
        )
    logger = logging.getLogger('tg_bot_logger')
    logger.setLevel(logging.INFO)
    handler = TelegramLogsHandler(
        logs_full_path,
        tg_bot=tg_bot,
        chat_id=chat_id,
        maxBytes=max_bytes,
        backupCount=backup_count,
    )
    logger.addHandler(handler)
    return logger


def create_parser():
    parser = argparse.ArgumentParser(
        description='Telegram bot sending tasks notifications',
    )
    parser.add_argument(
        '-ci',
        '--chat_id',
        type=str,
        metavar='',
        default=os.getenv('TG_CHAT_ID'),
        help='yours telegram chat id/user id',
    )
    parser.add_argument(
        '-d',
        '--dest_folder',
        type=str,
        metavar='',
        default=os.getenv('LOGS_FOLDER'),
        help='destination folder for bot logs service',
    )
    parser.add_argument(
        '-m',
        '--max_bytes',
        type=int,
        metavar='',
        default=200,
        help='maximum size bot.log file',
    )
    parser.add_argument(
        '-bc',
        '--backup_count',
        type=int,
        metavar='',
        default=2,
        help='bot logs backup counts',
    )
    return parser


def main():
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()

    dvmn_token = os.getenv('DVMN_TOKEN')
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    tg_chat_id = args.chat_id
    tg_bot = telegram.Bot(token=tg_bot_token)

    logger = create_logger(
        tg_bot,
        tg_chat_id,
        dest_folder=args.dest_folder,
        max_bytes=args.max_bytes,
        backup_count=args.backup_count,
    )
    logger.info('Bot started')

    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {dvmn_token}'
    }
    try:
        timestamp = time()
        while True:
            payload = {'timestamp': timestamp}
            try:
                response = requests.get(
                    url,
                    headers=headers,
                    params=payload,
                )
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logger.exception(e)
                continue
            except requests.exceptions.ReadTimeout:
                continue
            except requests.exceptions.ConnectionError as e:
                logger.exception(e)
                continue

            attempt_description = response.json()

            if attempt_description['status'] == 'timeout':
                timestamp = attempt_description['timestamp_to_request']
            else:
                timestamp = attempt_description['last_attempt_timestamp']
                last_attempt = attempt_description['new_attempts']
                lesson_title = last_attempt[-1]['lesson_title']
                lesson_url = last_attempt[-1]['lesson_url']
                attempt_is_negative = last_attempt[-1]['is_negative']
                if attempt_is_negative:
                    tg_bot.send_message(
                        chat_id=tg_chat_id,
                        text=(
                            f'У вас проверили работу "{lesson_title}".\n'
                            f'{lesson_url}\n\n'
                            'К сожалению в работе есть ошибки. '
                            'Исправляйте и возвращайтесь.'
                        ),
                    )
                else:
                    tg_bot.send_message(
                        chat_id=tg_chat_id,
                        text=(
                            f'У вас проверили работу "{lesson_title}".\n'
                            f'{lesson_url}\n\nПреподавателю всё понравилось,'
                            'можно приступать к следующему уроку'
                        ),
                    )
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()

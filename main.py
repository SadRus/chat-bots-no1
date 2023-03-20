import argparse
import os
import requests
import telegram

from dotenv import load_dotenv
from time import time


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
    return parser


def main():
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()

    dvmn_token = os.getenv('DVMN_TOKEN')
    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    tg_chat_id = args.chat_id

    bot = telegram.Bot(token=tg_bot_token)

    url = 'https://dvmn.org/api/long_polling/'
    headers = {
        'Authorization': f'Token {dvmn_token}'
    }

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
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            print('ConnectionError. Trying to reconnect...')
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
                bot.send_message(
                    chat_id=tg_chat_id,
                    text=(f'У вас проверили работу "{lesson_title}".\n'
                          f'{lesson_url}\n\n'
                          'К сожалению в работе есть ошибки. '
                          'Исправляйте и возвращайтесь.')
                )
            else:
                bot.send_message(
                    chat_id=tg_chat_id,
                    text=(f'У вас проверили работу "{lesson_title}".\n'
                          f'{lesson_url}\n\nПреподавателю всё понравилось,'
                          'можно приступать к следующему уроку')
                )


if __name__ == '__main__':
    main()

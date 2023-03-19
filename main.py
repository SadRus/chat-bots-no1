import argparse
import json
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
            print(response.text)
        except requests.exceptions.ReadTimeout:
            print('ReadTimeout')
        except requests.exceptions.ConnectionError:
            print('ConnectionError')

        attempt_description = json.loads(response.text)

        if attempt_description['status'] == 'timeout':
            timestamp = attempt_description['timestamp_to_request']
        else:
            timestamp = attempt_description['last_attempt_timestamp']
            lesson_title = attempt_description['new_attempts'][-1]['lesson_title']
            lesson_url = attempt_description['new_attempts'][-1]['lesson_url']
            attempt_is_negative = attempt_description['new_attempts'][-1]['is_negative']

            if attempt_is_negative:
                bot.send_message(
                    chat_id=tg_chat_id,
                    text=(f'У вас проверили работу "{lesson_title}".\n'
                          f'{lesson_url}\n\n'
                          'К сожалению в работе есть ошибки.'
                          ' Исправляйте и возвращайтесь.')
                )
            else:
                bot.send_message(
                    chat_id=tg_chat_id,
                    text=(f'У вас проверили работу "{lesson_title}".\n'
                          f'{lesson_url}\n\nПреподавателю всё понравилось,'
                          'можно приступать к следующему уроку')
                )


if __name__ == '__main__':
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()

    main()

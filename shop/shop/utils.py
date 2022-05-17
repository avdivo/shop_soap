# Как настроить приватный канал https://qna.habr.com/q/299390
import requests
from django.conf import settings

def message_to_telegram(message):
    bot_api_key = settings.BOT_API_KEY
    # channel_name = '@MessageGreenSoap'
    channel_id = settings.TELEGRAM_CHANEL_ID
    url = f'https://api.telegram.org/bot{bot_api_key}/sendMessage'

    params = {
        'chat_id': channel_id,
        'text': message,
    }
    print(requests.get(url, params=params).json())



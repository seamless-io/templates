import os

import requests

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')
BOT_API_KEY = os.getenv('BOT_API_KEY')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')

if __name__ == '__main__':
    resp = requests.get(
        f"https://api.openweathermap.org/data/2.5/onecall?lat={LATITUDE}&lon={LONGITUDE}&APPID={WEATHER_API_KEY}")
    forecast = resp.json()['daily'][0]
    today_weather = forecast['weather'][0]['description']
    if 'rain' in today_weather:
        requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage',
                     params={'chat_id': CHANNEL_NAME,
                             'text': 'It\'s going to rain today' + u'\U00002614' + ', take your umbrella with you!'})

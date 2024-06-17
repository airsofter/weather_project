import os
import time
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv
from yandexgptlite import YandexGPTLite

from sber_token import get_sber_token


load_dotenv()

genres = ['DRAMA', 'COMEDY', 'MUSICAL', 'DETECTIVE', 'ACTION', 'HORROR']

OpenWeatherMap_KEY = os.getenv('OpenWeatherMap_KEY')
YANDEX_KEY = os.getenv('YANDEX_KEY')
CATALOG_ID_YANDEX = os.getenv('CATALOG_ID_YANDEX')
SBER_TOKEN = os.getenv('SBER_TOKEN')
SBER_AUTHORIZATION = os.getenv('SBER_AUTHORIZATION')

yandex_account = YandexGPTLite(folder=CATALOG_ID_YANDEX, token=YANDEX_KEY)


def get_location(city_name):
    '''Используем Geocoding API для поиска геолокации'''
    url = (
        f'http://api.openweathermap.org/geo/1.0/direct?q={city_name}'
        f'&limit=1&appid={OpenWeatherMap_KEY}'
    )
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]["lat"], data[0]["lon"]
    else:
        raise ValueError("Город не найден")


def get_forecast(lat, lon):
    '''Используем Weather API для получения прогноза погоды'''
    url = (
        f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&'
        f'lon={lon}&units=metric&appid={OpenWeatherMap_KEY}&lang=ru'
    )
    response = requests.get(url)
    data = response.json()
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_date_str = tomorrow.strftime('%Y-%m-%d')
    for forecast in data['list']:
        forecast_time = datetime.fromtimestamp(forecast['dt'])
        if forecast_time.strftime('%Y-%m-%d') == tomorrow_date_str:
            return forecast


def generate_prompt(city, genre, weather):
    '''Составляем промпт для нейросети'''
    weather_desc = weather['weather'][0]['description']
    temp_min = weather['main']['temp_min']
    temp_max = weather['main']['temp_max']
    pressure = weather['main']['pressure']
    clouds = weather['clouds']['all']
    prompt = (
        f'Придумай сказку в жанре {genre} о погоде в городе {city} на завтра. '
        f'Завтра будет {weather_desc} с температурой '
        f'от {temp_min} до {temp_max} градусов. '
        f'Давление - {pressure}, облачность в процентах - {clouds}.'
    )
    return prompt


def get_story_from_gigachat(prompt, max_length):
    '''Запрос к GigaChat'''
    if int(time.time() * 1000) >= int(os.getenv('SBER_TIME_TOKEN')):
        get_sber_token(SBER_AUTHORIZATION)
    token = os.getenv('SBER_TOKEN')
    gigachat_api_url = (
        'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
    )
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    data = {
        'model': 'GigaChat',
        'messages': [
            {
                'role': 'system',
                'content': 'Сгенерируй сказку.'
            },
            {
                'role': 'user',
                'content': prompt
            },
        ],
        'temperature': 0.9,
        'stream': False,
        'max_tokens': max_length,
    }
    start_time = time.time()
    response = requests.post(
        gigachat_api_url, headers=headers, json=data, verify=False
    )
    end_time = time.time()
    duration = end_time - start_time
    story = response.json()['choices'][0]['message']['content']
    print(story)
    return story, duration


def get_story_from_yandex(prompt, max_length):
    '''Запрос к яндекс GPT'''
    start_time = time.time()
    story = yandex_account.create_completion(
        prompt=prompt,
        system_prompt='Сгенерируй сказку.',
        max_tokens=max_length,
        temperature='0.9'
    )
    end_time = time.time()
    duration = end_time - start_time
    print(story)
    return story, duration


def main():
    city = input('Введите город: ')
    genre = input(f'Введите жанр из перечисленных {genres}: ')
    if genre.upper() not in genres:
        raise ValueError('Такого жанра нет!')
    max_length = int(input('Введите длину сказки в словах: '))

    lat, lon = get_location(city)
    weather = get_forecast(lat, lon)
    prompt = generate_prompt(city, genre, weather)

    yandex_story, yandex_duration = get_story_from_yandex(
        prompt, max_length
    )

    gigachat_story, gigachat_duration = get_story_from_gigachat(
        prompt, max_length
    )

    with open("yandex_story.txt", "w", encoding="utf-8") as f:
        f.write(yandex_story)
    with open("gigachat_story.txt", "w", encoding="utf-8") as f:
        f.write(gigachat_story)

    print(
        f'YandexGPT: Длительность запроса - {yandex_duration:.2f}'
        f'секунд, файл - yandex_story.txt')
    print(
        f'GigaChat: Длительность запроса - {gigachat_duration:.2f} '
        f'секунд, файл - gigachat_story.txt'
     )


if __name__ == "__main__":
    main()

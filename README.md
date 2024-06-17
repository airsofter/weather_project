## Программа для создания сказки о погоде

### Описание

Программа получает на вход через консоль название города на любом языке в любом регистре. Жанр произведения и его ограничение по количеству слов. 
На основе этих данных составляется рассказ о погоде на завтрашний день в заданном городе.
В консоль возвращается название задействованных языковых моделей, длительность запроса к каждой из них и название каждого файла, в которые происходит сохранение рассказов

### Используемые API
- Geocoding API
- Weather API
- GigaChat API
- YandexGPT API

### Запуск

Необходимо клонировать репозиторий и перейти в корневую папку:
```
git clone git@github.com:airsofter/weather_story
cd weather_story
```

Установите необходимые библиотеки с помощью Poetry
```
poetry install
```

Создать в корневой папке файл .env с переменными окружения, необходимыми 
для работы приложения. Разместить этот файл в папке проекта weather_story.

OpenWeatherMap_KEY=
YANDEX_KEY=y0_AgAAA
CATALOG_ID_YANDEX=
SBER_AUTHORIZATION=

Данные для файла нужно получить в соответсвующих сервисах.
Документация для получения ключа OpenWeatherMap_KEY - https://openweathermap.org/appid
Нужно будет скопировать ключ из личного кабинета в переменную.

Документация для SBER_AUTHORIZATION https://developers.sber.ru/docs/ru/gigachat/individuals-quickstart
Необходимый ключ вы найдете в личном кабинете в строке "Авторизационные данные"

Документация для получения ключей от Яндекс GPT - https://yandex.cloud/ru/docs/iam/operations/iam-token/create#bash_1
Для получения ключа CATALOG_ID_YANDEX нужно перейти в раздел "консоль" на сервисе и 
скипировать ID каталога в переменную.
Для получения YANDEX_KEY необходимо перейти по ссылке из 2 пункта документации Яндекса и скопировать ключ в переменную

После всех действий с ключами, можно запустить программу

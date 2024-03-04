import requests
import json
import datetime
from config import API_OWM


# Функция для определения направления ветра
async def wind_direction(data):
    direct = ''
    degrees = round(int(data["wind"]["deg"]))
    if (338 <= degrees <= 360) or (0 <= degrees <= 23):
        direct = 'С'
    elif 158 <= degrees <= 203:
        direct = 'Ю'
    elif 248 <= degrees <= 293:
        direct = 'З'
    elif 68 <= degrees <= 113:
        direct = 'В'
    elif 23 < degrees < 68:
        direct = 'СВ'
    elif 293 < degrees < 338:
        direct = 'СЗ'
    elif 113 < degrees < 158:
        direct = 'ЮВ'
    elif 203 < degrees < 248:
        direct = 'СЗ'
    return direct


# Функция для определения погоды в определенном городе
async def city_weather(message):
    city = message.lower().strip()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_OWM}&units=metric&lang=ru')
    if res.status_code == 200:
        data = json.loads(res.text)
        return f'Текущая погода в городе {city.capitalize()}:\n• {(data["weather"][0]["description"]).capitalize()}\n• {round(data["main"]["temp"])}°C <em>(Ощущается как: {round(data["main"]["feels_like"])}°C)</em>\n• Давление: {round((data["main"]["pressure"]) / 1.33)} мм.рт.ст.\n• Влажность: {data["main"]["humidity"]}%\n• Ветер: {round(data["wind"]["speed"])} м/с ({await wind_direction(data)})'
    else:
        return 'Город указан неверно'


# Функция для определения погоды на несколько дней
async def weather_for_several_days(message):
    city = message.lower().strip()
    res = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_OWM}&units=metric&lang=ru')
    if res.status_code == 200:
        data = res.json()
        response = ''
        for elem in data['list']:
            if elem['dt_txt'][:10] in [str(datetime.datetime.now() + datetime.timedelta(days=1))[:10],
                                       str(datetime.datetime.now() + datetime.timedelta(days=2))[:10],
                                       str(datetime.datetime.now() + datetime.timedelta(days=3))[:10],
                                       str(datetime.datetime.now() + datetime.timedelta(days=4))[:10]]:
                time = int(elem['dt_txt'][-8:-6]) + int(data['city']['timezone']) // 3600
                if time in [14, 15, 16]:
                    response += f'Днем: {round(int(elem["main"]["temp"]))}°C\n\n'
                elif time in [2, 3, 4]:
                    response += f'Погода в городе {city.capitalize()} на {elem["dt_txt"][8:10]}.{elem["dt_txt"][5:7]}.{elem["dt_txt"][2:4]}:\n{elem["weather"][0]["description"].capitalize()}\nНочью: {round(int(elem["main"]["temp"]))}°C\n'
        return response
    else:
        return 'Город указан неверно'


# Функция для определения погоды на весь день
async def weather_for_day(message):
    city = message
    res = requests.get(f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_OWM}&units=metric&lang=ru')
    if res.status_code == 200:
        data = res.json()
        response = ''
        for elem in data['list']:
            if elem['dt_txt'][:10] in [str(datetime.datetime.now() + datetime.timedelta(days=1))[:10]]:
                time = int(elem['dt_txt'][-8:-6]) + int(data['city']['timezone']) // 3600
                if time in [14, 15, 16]:
                    response += f'Днем: {round(int(elem["main"]["temp"]))}°C\n\n'
                elif time in [2, 3, 4]:
                    response += f'Погода в городе {city.capitalize()} на {elem["dt_txt"][8:10]}.{elem["dt_txt"][5:7]}.{elem["dt_txt"][2:4]}:\n{elem["weather"][0]["description"].capitalize()}\nНочью: {round(int(elem["main"]["temp"]))}°C\n'
        return response
    else:
        return 'Город указан неверно'


# Функция для определения погоды в определенный момент времени по местоположению пользователя
async def now_weather_location(lat, lon):
    res = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_OWM}&units=metric&lang=ru')
    if res.status_code == 200:
        data = json.loads(res.text)
        return f'Текущая погода в городе {data["name"]}\n• {(data["weather"][0]["description"]).capitalize()}\n• {round(data["main"]["temp"])}°C <em>(Ощущается как: {round(data["main"]["feels_like"])}°C)</em>\n• Давление: {round((data["main"]["pressure"]) / 1.33)} мм.рт.ст.\n• Влажность: {data["main"]["humidity"]}%\n• Ветер: {round(data["wind"]["speed"])} м/с ({await wind_direction(data)})'
    else:
        return 'Ошибка в геопозиции'


# Функция для прогноза погоды на несколько дней по местоположению
async def several_weather_location(lat, lon):
    res = requests.get(
        f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_OWM}&units=metric&lang=ru')
    if res.status_code == 200:
        data = res.json()
        response = ''
        for elem in data['list']:
            if elem['dt_txt'][:10] in [str(datetime.datetime.now() + datetime.timedelta(days=1))[:10],
                                       str(datetime.datetime.now() + datetime.timedelta(days=2))[:10],
                                       str(datetime.datetime.now() + datetime.timedelta(days=3))[:10],
                                       str(datetime.datetime.now() + datetime.timedelta(days=4))[:10]]:
                time = int(elem['dt_txt'][-8:-6]) + int(data['city']['timezone']) // 3600
                if time in [14, 15, 16]:
                    response += f'Днем: {round(int(elem["main"]["temp"]))}°C\n\n'
                elif time in [2, 3, 4]:
                    response += f'Погода в городе {data["city"]["name"]} на {elem["dt_txt"][8:10]}.{elem["dt_txt"][5:7]}.{elem["dt_txt"][2:4]}:\n{elem["weather"][0]["description"].capitalize()}\nНочью: {round(int(elem["main"]["temp"]))}°C\n'
        return response
    else:
        return 'Город указан неверно'


# Функция для проверки существования города по местоположению
async def location_city_exist(lat, lon):
    res = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_OWM}&units=metric&lang=ru')
    if res.status_code == 200:
        data = json.loads(res.text)
        return data['name']
    else:
        return False


# Функция для проверки существования города по сообщению
async def message_city_exist(message):
    city = message.text.lower().strip()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_OWM}&units=metric&lang=ru')
    if res.status_code == 200:
        data = json.loads(res.text)
        return data['name']
    else:
        return False

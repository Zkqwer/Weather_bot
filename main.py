from aiogram import Bot, Dispatcher, executor, types
import asyncio
import datetime
import pytz
from config import TELEGRAM_API
import database
import keyboards
import owm_data

bot = Bot(token=TELEGRAM_API)
dp = Dispatcher(bot)


# Функция вывода сообщения о том, что бот успешно запущен
async def on_startup(_):
    await database.delete_tables()
    await database.create_tables()
    print('bot start successfully')


# Функция отвечающая за запуск бота (команду start)
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        text=f'Привет, {message.from_user.first_name}, это чат бот который пришлет тебе данные о погоде',
             reply_markup=keyboards.kb_start_keyboard)


# Функция для определения координат по местоположению которое отправил пользователь, применение их в функциях owm_data
@dp.message_handler(content_types=['location'])
async def user_location(message):
    user = await database.get_user_by_id(message.chat.id)
    if message.location is not None:
        lat = message.location.latitude
        lon = message.location.longitude
        if user['step'] == 'weather now':
            await message.answer(await owm_data.now_weather_location(lat, lon), parse_mode="html")
        elif user['step'] == 'weather for several days':
            await message.answer(await owm_data.several_weather_location(lat, lon), parse_mode="html")
        elif user['step'] == 'adding a city to the database':
            city = await owm_data.location_city_exist(lat, lon)
            if city:
                await database.update_user_city(message.chat.id, city)
                await message.answer('Город успешно добавлен')


# Функция (уведомлений) для отправки погоды в соответствии с выбранным временем
async def notifications(message):
    moscow_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    notification_time = (datetime.datetime.strptime(str(moscow_time)[:11] + message.text, '%Y-%m-%d %H:%M')).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=3)))
    sleep_time = (notification_time - moscow_time).total_seconds()
    if sleep_time < 0:
        sleep_time += 24 * 60 * 60
    while True:
        await asyncio.sleep(sleep_time)
        user = await database.get_user_by_id(message.chat.id)
        if user['notifications'] == 1:
            await message.answer(text=f'Уведомление о погоде\n{await owm_data.weather_for_day(user["city"])}', parse_mode="html")
        else:
            return
        sleep_time = 24 * 60 * 60


# Логика работы бота
@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    # Получаем информацию о пользователе из базы данных
    user = await database.get_user_by_id(message.chat.id)
    # Если пользователя нет в базе данных, то добавляем его
    if user is None:
        await database.add_new_user(message.chat.id)
        user = await database.get_user_by_id(message.chat.id)

    if message.text == 'Меню':
        await message.answer(text='Выбери действие, чтобы продолжить',
                             reply_markup=keyboards.kb_menu)
        await database.update_user_step(message.chat.id, step='0')

    elif message.text == 'Назад':
        if user['step'] in ['weather now', 'settings', 'weather for several days', '0', 'weather for several days select city', 'weather now select city']:
            await database.update_user_step(message.chat.id, step='0')
            await message.answer(text='Выбери действие, чтобы продолжить',
                             reply_markup=keyboards.kb_menu)
        elif user['step'] in ['notifications', 'set notifications', 'adding a city to the database']:
            await message.answer(text='Чтобы продолжить, выбери действие ниже',
                                 reply_markup=keyboards.kb_settings)
            await database.update_user_step(message.chat.id, step='settings')

    elif message.text == 'Погода сейчас':
        await message.answer(text='Выбери действие, чтобы продолжить', reply_markup=keyboards.kb_city_definition)
        await database.update_user_step(message.chat.id, step='weather now')

    elif user['step'] == 'weather now':
        if message.text == 'Мой город':
            if user['city'] == '0':
                await message.answer(text='Чтобы воспользоваться этой функцией, укажи свой город в настройках')
            else:
                await message.answer(await owm_data.city_weather(user['city']), parse_mode="html")
        elif message.text == 'Выбрать город':
            await message.answer(text='Введи город')
            await database.update_user_step(message.chat.id, step='weather now select city')
        else:
            await message.answer(text='Неизвестная команда')

    elif user['step'] == 'weather now select city':
        if message.text == 'Мой город':
            if user['city'] == '0':
                await message.answer(text='Чтобы воспользоваться этой функцией, укажи свой город в настройках')
            else:
                await message.answer(await owm_data.city_weather(user['city']), parse_mode="html")
        else:
            weather_forecast = await owm_data.city_weather(message.text)
            await message.answer(weather_forecast, parse_mode="html")

    elif message.text == 'Погода на 4 дня':
        await message.answer(text='Выбери действие, чтобы продолжить', reply_markup=keyboards.kb_city_definition)
        await database.update_user_step(message.chat.id, step='weather for several days')

    elif user['step'] == 'weather for several days':
        if message.text == 'Мой город':
            if user['city'] == '0':
                await message.answer(text='Чтобы воспользоваться этой функцией, укажи свой город в настройках')
            else:
                await message.answer(await owm_data.weather_for_several_days(user['city']), parse_mode="html")
        elif message.text == 'Выбрать город':
            await message.answer(text='Введи город')
            await database.update_user_step(message.chat.id, step='weather for several days select city')
        else:
            await message.answer(text='Неизвестная команда')

    elif user['step'] == 'weather for several days select city':
        if message.text == 'Мой город':
            if user['city'] == '0':
                await message.answer(text='Чтобы воспользоваться этой функцией, укажи свой город в настройках')
            else:
                await message.answer(await owm_data.weather_for_several_days(user['city']), parse_mode="html")
        else:
            weather_forecast = await owm_data.weather_for_several_days(message.text)
            await message.answer(weather_forecast, parse_mode="html")

    elif message.text == 'Настройки':
        await message.answer(text='Чтобы продолжить, выбери действие ниже',
                             reply_markup=keyboards.kb_settings)
        await database.update_user_step(message.chat.id, step='settings')

    elif message.text == 'Уведомления':
        await message.answer(text='Выбери действие, чтобы продолжить', reply_markup=keyboards.kb_notifications)
        await database.update_user_step(message.chat.id, 'notifications')

    elif message.text == 'Подключить уведомления':
        if user['city'] == '0':
            await message.answer(text='Для начала введи свой город в настройках')
        else:
            await message.answer(text='Введи время по мск, в которое ты хочешь получать уведомления, в формате чч:мм')
            await database.update_user_step(message.chat.id, step='set notifications')
            await database.update_user_notifications(message.chat.id, notifications=1)

    elif message.text == 'Отключить уведомления':
        await database.update_user_notifications(message.chat.id, notifications=0)
        await message.answer(text='Уведомления отключены')

    elif user['step'] == 'set notifications':
        if message.text.count(':') != 1 or not message.text.split(':')[0].isdigit() or not message.text.split(':')[
            1].isdigit() \
                or int(message.text.split(':')[0]) > 24 or int(message.text.split(':')[0]) < 0 or int(
            message.text.split(':')[1]) > 59 or int(message.text.split(':')[0]) < 0:
            await message.answer(text='Неверно указано время')
        else:
            await message.answer(text='Время успешно сохранено')
            await notifications(message)

    elif user['step'] == 'settings' and message.text == 'Мой город':
        if user['city'] == '0':
            await message.answer(text='У тебя нет сохраненного города', reply_markup=keyboards.kb_my_city)
        else:
            await message.answer(text=f'Твой город: {user["city"]}', reply_markup=keyboards.kb_my_city)

    elif message.text == 'Изменить город':
        await message.answer(text='Напиши название своего города или отправь свою геолокацию',
                             reply_markup=keyboards.kb_city_memory)
        await database.update_user_step(message.chat.id, step='adding a city to the database')

    elif user['step'] == 'adding a city to the database':
        if await owm_data.message_city_exist(message):
            await database.update_user_city(message.chat.id, message.text)
            await message.answer(text='Город успешно добавлен')
        else:
            await message.answer(text='Город не найден')

    else:
        await message.answer(text='Нет такой команды')
        await database.update_user_step(message.chat.id, step='0')


# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp,
                           on_startup=on_startup,
                           skip_updates=True)

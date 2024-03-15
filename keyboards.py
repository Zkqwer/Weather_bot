from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Общие кнопки
btn_back = KeyboardButton(text="Назад")
btn_location = KeyboardButton(text="Отправить местоположение", request_location=True)
btn_weather = KeyboardButton(text="Погода")
btn_settings = KeyboardButton(text="Настройки")
btn_menu = KeyboardButton(text="Меню")


# Кнопка для команды start
kb_start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
kb_start_keyboard.add(btn_menu)

# Кнопки для меню
kb_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_weather_now = KeyboardButton(text="Погода сейчас")
btn_weather_week = KeyboardButton(text="Погода на 4 дня")
kb_menu.add(btn_weather_now, btn_weather_week, btn_settings)

# Кнопки для функции city_definition
kb_city_definition = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_user_city = KeyboardButton(text="Мой город")
btn_select_city = KeyboardButton(text="Выбрать город")
kb_city_definition.add(btn_select_city, btn_location, btn_user_city, btn_back)

# Кнопки для сохранения города
kb_my_city = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
btn_change_city = KeyboardButton(text="Изменить город")
kb_my_city.add(btn_change_city, btn_back)

# Кнопки для настроек
kb_settings = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn_notification = KeyboardButton(text="Уведомления")
btn_remember_user_city = KeyboardButton(text="Мой город")
kb_settings.add(btn_remember_user_city, btn_notification, btn_back)

# Кнопки для уведомлений
kb_notifications = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
btn_put_on_notice = KeyboardButton(text="Подключить уведомления")
btn_put_off_notice = KeyboardButton(text="Отключить уведомления")
kb_notifications.add(btn_put_on_notice, btn_put_off_notice, btn_back)

# Кнопки для функции city_memory
kb_city_memory = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
kb_city_memory.add(btn_location, btn_back)

# Кнопки для функции kb_notification
kb_notification = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kb_notification.add(btn_weather, btn_settings)

# Кнопки для функции selected_city
kb_selected_city = ReplyKeyboardMarkup(resize_keyboard=True)
kb_selected_city.add(btn_location, btn_back)

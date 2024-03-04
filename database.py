import sqlite3 as sq

db = sq.connect('cities.db')
cursor = db.cursor()


# Создание таблицы
async def create_tables():
    cursor.execute("CREATE TABLE IF NOT EXISTS users("
                   "user_id INTEGER PRIMARY KEY, "
                   "step TEXT, "
                   "city TEXT, "
                   "notifications INTEGER)")
    db.commit()


# Удаление таблицы
async def delete_tables():
    cursor.execute("DROP TABLE IF EXISTS users")
    db.commit()


# Добавление нового пользователя в таблицу
async def add_new_user(user_id):
    cursor.execute(f"INSERT INTO users (user_id, step, city, notifications) VALUES ({user_id}, '0', '0', 0)")
    db.commit()


# Изменение этапа пользователя
async def update_user_step(user_id, step):
    cursor.execute(f"UPDATE users SET step = '{step}' WHERE user_id == {user_id}")
    db.commit()


# По аналогии с update_user_step функция для изменения значения города и уведомлений
async def update_user_city(user_id, city):
    cursor.execute(f"UPDATE users SET city = '{city}' WHERE user_id == {user_id}")
    db.commit()


# Сохранение времени для уведомлений, выбранное пользователем
async def update_user_notifications(user_id, notifications):
    cursor.execute(f"UPDATE users SET notifications = '{notifications}' WHERE user_id == {user_id}")
    db.commit()


# Получение информации о пользователе
async def get_user_by_id(user_id):
    user = cursor.execute(f"SELECT * FROM users WHERE user_id == {user_id}").fetchone()
    if user is None:
        return None
    res = {'user_id': None, 'step': None, 'city': None, 'notifications': None}
    res_keys = ['user_id', 'step', 'city', 'notifications']
    for i in range(len(user)):
        res[res_keys[i]] = user[i]
    return res

import sqlite3 as sq
from peewee import sqlite3
from database.models.models_main import db


# получение определенного количества строк из БД посредством проверки по user_id
def read_limited_characters_page(user_id):
    global base
    try:
        base = sq.connect('dnd.db')
        cursor = base.cursor()
        query = "SELECT * FROM Characters WHERE user_id = " + str(user_id)
        cursor.execute(query)
        record = cursor.fetchall()
        cursor.close()
        return record

    except sqlite3.Error as error:
        print("Ошибка в работе с SQLite ", error)
    finally:
        if base:
            base.close()

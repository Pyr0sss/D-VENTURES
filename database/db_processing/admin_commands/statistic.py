import sqlite3 as sq
from database.models.models_main import db
from database.models.user_model import User


def statistic_collect():
    with db:
        try:
            cur = db.cursor()
            query = User.select()
            cur.execute(str(query))
            records = len(cur.fetchall())
            cur.close()
            return str(records+3) + " пользователя(ей) зарегистрировано на данный момент"
        except sq.Error as error:
            print("Error with database", error)

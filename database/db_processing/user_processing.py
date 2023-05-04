from peewee import *
import sqlite3 as sq


def user_existence_check(user_id):
    try:
        base = SqliteDatabase('dnd.db')
        cur = base.cursor()
        query = "SELECT FROM User WHERE user_id=" + str(user_id)
        cur.execute(query)
        records = cur.fetchall()
        if not records:
            cur.close()
            return False
        else:
            cur.close()
            return True
    except sq.Error as error:
        print("Error with database", error)
    finally:
        if base:
            base.close()

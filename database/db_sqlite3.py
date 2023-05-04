import sqlite3 as sq

from peewee import *

try:
    base = SqliteDatabase('dnd.db')
    cur = base.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users")
    cur.execute("CREATE TABLE IF NOT EXISTS Characters")
    cur = base.cursor()
except sq.Error as error:
    print("Error with database", error)
finally:
    if base:
        base.close()



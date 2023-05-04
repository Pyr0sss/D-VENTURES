import sqlite3 as sq

from peewee import *

base = SqliteDatabase('dnd.db')
cur = base.cursor()
#cur.execute("CREATE TABLE IF NOT EXISTS Characters(id INT PRIMARY KEY, name TEXT, race TEXT, class TEXT, origin TEXT, level INT)")
#base.commit()



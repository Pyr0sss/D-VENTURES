from peewee import *

db = SqliteDatabase('dnd.db')
db.connect()

class BaseModel(Model):
    class Meta:
        database = db



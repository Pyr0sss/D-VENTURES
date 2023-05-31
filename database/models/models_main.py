import config
from peewee import *

db = SqliteDatabase(config.current_db_name)
db.connect()

class BaseModel(Model):
    class Meta:
        database = db



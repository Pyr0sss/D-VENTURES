from peewee import *
from database.models.models_main import BaseModel

class Character(BaseModel):
    user_id = IntegerField(column_name="user_id")
    character_id = AutoField(column_name="character_id")
    name = TextField(column_name="name")
    race = TextField(column_name="race")
    clas = TextField(column_name="clas")
    origin = TextField(column_name="origin")
    level = IntegerField(column_name="level")
    class Meta:
        table_name = "Characters"
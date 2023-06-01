from peewee import *
from database.models.models_main import BaseModel

class User(BaseModel):
    user_id = IntegerField(column_name="user_id")
    username = TextField(column_name="username")
    is_banned = CharField(column_name="is_banned")
    class Meta:
        table_name = "Users"
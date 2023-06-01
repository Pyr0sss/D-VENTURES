from peewee import *
from database.models.models_main import BaseModel

class Quality(BaseModel):
    user_id = IntegerField(column_name="user_id")
    character_id=IntegerField(column_name="character_id")
    force=IntegerField(column_name="force")
    agility=IntegerField(column_name="agility")
    body=IntegerField(column_name="body")
    intellect=IntegerField(column_name="intellect")
    wisdom=IntegerField(column_name="wisdom")
    charisma=IntegerField(column_name="charisma")
    class Meta:
        table_name = "Qualities"
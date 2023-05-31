from peewee import *
from database.models.models_main import BaseModel

class Race(BaseModel):
    race_id = AutoField(column_name="race_id")
    race_name = TextField(column_name="race_name")
    race_description = TextField(column_name="race_description")
    class Meta:
        table_name = "Races"
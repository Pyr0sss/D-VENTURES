from peewee import *
from database.models.models_main import BaseModel

class Origin(BaseModel):
    origin_id = AutoField(column_name="origin_id")
    origin_name = TextField(column_name="origin_name")
    origin_description = TextField(column_name="origin_description")
    class Meta:
        table_name = "Origins"
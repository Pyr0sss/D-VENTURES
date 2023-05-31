from peewee import *
from database.models.models_main import BaseModel

class Clas(BaseModel):
    clas_id = AutoField(column_name="class_id")
    clas_name = TextField(column_name="class_name")
    clas_description = TextField(column_name="class_description")
    class Meta:
        table_name = "Classes"
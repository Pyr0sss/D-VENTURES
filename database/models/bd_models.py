from peewee import *
from database.db_sqlite3 import base

class BaseModel(Model):
    class Meta:
        database = base

class User(BaseModel):
    user_id = IntegerField(column_name="user_id")
    class Meta:
        table_name = "users"

class Character(BaseModel):
    player_id = AutoField(column_name="player_id")
    user_id = IntegerField(column_name="user_id")
    name = TextField(column_name="name")
    clas = TextField(column_name="class")
    origin = TextField(column_name="origin")
    level = IntegerField(column_name="level")
    class Meta:
        table_name = "Characters"

class Spell(BaseModel):
    spell_id = AutoField(column_name="spell_id")
    spell_name = TextField(column_name="spell_name")
    level = IntegerField(column_name="spell_level")
    class_wizard = CharField(column_name="wizards")
    class_warlock = CharField(column_name="warlocks")
    class_sorcerer = CharField(column_name="sorcerers")
    class_bard = CharField(column_name="bards")
    class_cleric = CharField(column_name="clerics")
    class_druid = CharField(column_name="druids")
    class_paladin = CharField(column_name="paladins")
    class_artificer = CharField(column_name="artificers")
    class_ranger = CharField(column_name="rangers")



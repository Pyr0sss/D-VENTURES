from peewee import *
from database.models.models_main import BaseModel

class Spell(BaseModel):
    spell_id = AutoField(column_name="spell_id")
    spell_name = TextField(column_name="spell_name")
    level = IntegerField(column_name="level")
    class_wizard = CharField(column_name="wizards")
    class_warlock = CharField(column_name="warlocks")
    class_sorcerer = CharField(column_name="sorcerers")
    class_bard = CharField(column_name="bards")
    class_cleric = CharField(column_name="clerics")
    class_druid = CharField(column_name="druids")
    class_paladin = CharField(column_name="paladins")
    class_artificer = CharField(column_name="artificers")
    class_ranger = CharField(column_name="rangers")
    description = TextField(column_name="description")
    class Meta:
        table_name = "Spells"
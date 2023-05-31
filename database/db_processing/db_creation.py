from database.models.models_main import db
from database.models.character_model import Character
from database.models.user_model import User
from database.models.race_model import Race
from database.models.spell_model import Spell
from database.models.class_model import Clas
from database.models.origin_model import Origin


def db_creation():
    with db:
        db.create_tables([User, Character, Race, Spell, Clas, Origin])

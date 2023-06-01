import sqlite3 as sq
from database.models.models_main import db
from database.models.spell_model import Spell


def get_spell_info(spell_id):
    with db:
        try:
            cur = db.cursor()
            query = Spell.select().where(Spell.spell_id == spell_id)
            cur.execute(str(query))
            records = cur.fetchall()
            return records
        except sq.Error as error:
            print("Error with database", error)


def get_total_spells():
    with db:
        try:
            cur = db.cursor()
            query = Spell.select()
            cur.execute(str(query))
            records = len(cur.fetchall())
            cur.close()
            return records
        except sq.Error as error:
            print("Error with database", error)


def search_spell_by_name(name):
    with db:
        try:
            cur = db.cursor()
            query = f"SELECT * FROM Spells WHERE spell_name LIKE '{name}%' COLLATE NOCASE"
            print(query)
            cur.execute(str(query))
            records = cur.fetchall()
            cur.close()
            return records
        except sq.Error as error:
            print("Error with database", error)


def search_spell_for_character(clas, level):
    classes = {'Бард 🪕': 'bards', 'Чародей 🔮': 'wizards', 'Колдун 🧿': 'warlocks', 'Волшебник 📖': 'sorcerers', 'Жрец ⚕': 'clerics',
               'Друид 🌳': 'druids', 'Паладин 🛡️': 'paladins', 'Изобретатель ⚙': 'artificers', 'Следопыт 🔎': 'rangers', 'Плут 🧤': 'rangers', 'Монах ⛪': 'rangers',
               'Варвар 🪓': 'paladins', 'Воин ⚔': 'paladins'}
    with db:
        try:
            cur = db.cursor()
            query = f"SELECT * FROM Spells WHERE level <= {level} AND {classes.get(clas)} = 1"
            cur.execute(str(query))
            records = cur.fetchall()
            cur.close()
            return records
        except sq.Error as error:
            print("Error with database", error)

from unittest import TestCase
from peewee import SqliteDatabase

import config
config.current_db_name = config.test_db_path

from database.models.spell_model import Spell
from database.db_processing.spell_create import new_spell
from database.db_processing.spell_delete import del_spell


class SpellTests(TestCase):

    def setUp(self) -> None:
        self.db = SqliteDatabase(config.test_db_path)
        self.db.connect()
        with self.db:
            self.db.create_tables([Spell])
        cursor = self.db.cursor()
        query = "DELETE FROM Spells"
        cursor.execute(query)

    def get_all_spells(self):
        with self.db:
            cur = self.db.cursor()
            query = Spell.select()
            cur.execute(str(query))
            records = cur.fetchall()
            cur.close()
            return records

    def test_new_spell_1class(self):
        new_spell("новый спелл", 3, ["class_wizard"], "some text")
        actual_spell = self.get_all_spells()[0]
        expected_spell = (1, "новый спелл", 3, '1', '0', '0', '0', '0', '0', '0', '0', '0', 'some text')
        self.assertEquals(expected_spell, actual_spell)

    def test_new_spell_2class(self):
        new_spell("новый2 спелл", 10, ["class_wizard", "class_paladin"], "some text")
        actual_spell = self.get_all_spells()[0]
        expected_spell = (1, "новый2 спелл", 10, '1', '0', '0', '0', '0', '0', '1', '0', '0', 'some text')
        self.assertEquals(expected_spell, actual_spell)

    def test_delete_spell(self):
        Spell.create(spell_name="delete me", level=2, class_wizard='1', class_warlock='0',
                     class_sorcerer='0',
                     class_bard='0', class_cleric='0', class_druid='0', class_paladin='0',
                     class_artificer='0', class_ranger='0', description='1234')
        del_spell(1)
        self.assertEquals(0, len(self.get_all_spells()))
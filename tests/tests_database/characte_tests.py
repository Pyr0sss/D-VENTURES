from unittest import TestCase
from peewee import SqliteDatabase

import config
config.current_db_name = config.test_db_path

from database.models.character_model import Character
from database.db_processing.character_processing import *


class SpellTests(TestCase):

    def setUp(self) -> None:
        self.db = SqliteDatabase(config.test_db_path)
        self.db.connect()
        with self.db:
            self.db.create_tables([Character])
        cursor = self.db.cursor()
        query = "DELETE FROM Characters"
        cursor.execute(query)

    def get_all_characters(self):
        with self.db:
            cur = self.db.cursor()
            query = Character.select()
            cur.execute(str(query))
            records = cur.fetchall()
            cur.close()
            return records

    def test_new_character(self):
        create_character("name", 'race', ["class_wizard"], "some text")
        actual_character = self.get_all_characters()[0]
        expected_character = (1, "новый спелл", 3, '1', '0', '0', '0', '0', '0', '0', '0', '0', 'some text')
        self.assertEquals(expected_character, actual_character)

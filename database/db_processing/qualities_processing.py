import sqlite3 as sq
from database.models.models_main import db
from database.models.qualities_model import Quality


def get_qualities_info(qualities_id):
    with db:
        try:
            cur = db.cursor()
            query = Quality.select().where(Quality.character_id == qualities_id)
            cur.execute(str(query))
            records = cur.fetchall()
            return records
        except sq.Error as error:
            print("Error with database", error)


def get_total_qualities(id):
    with db:
        try:
            cur = db.cursor()
            query = Quality.select().where(Quality.character_id == id)
            cur.execute(str(query))
            records = len(cur.fetchall())
            cur.close()
            return records
        except sq.Error as error:
            print("Error with database", error)

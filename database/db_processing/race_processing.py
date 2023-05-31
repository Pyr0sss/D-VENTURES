import sqlite3 as sq
from database.models.models_main import db
from database.models.race_model import Race


def get_race_info(race_id):
    with db:
        try:
            cur = db.cursor()
            query = Race.select().where(Race.race_id == race_id)
            cur.execute(str(query))
            records = cur.fetchall()
            return records
        except sq.Error as error:
            print("Error with database", error)


def get_total_races():
    with db:
        try:
            cur = db.cursor()
            query = Race.select()
            cur.execute(str(query))
            records = len(cur.fetchall())
            cur.close()
            return records
        except sq.Error as error:
            print("Error with database races", error)

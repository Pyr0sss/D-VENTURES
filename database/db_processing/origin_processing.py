import sqlite3 as sq
from database.models.models_main import db
from database.models.origin_model import Origin


def get_origin_info(origin_id):
    with db:
        try:
            cur = db.cursor()
            query = Origin.select().where(Origin.origin_id == origin_id)
            cur.execute(str(query))
            records = cur.fetchall()
            return records
        except sq.Error as error:
            print("Error with database", error)


def get_total_origins():
    with db:
        try:
            cur = db.cursor()
            query = Origin.select()
            cur.execute(str(query))
            records = len(cur.fetchall())
            cur.close()
            return records
        except sq.Error as error:
            print("Error with database", error)

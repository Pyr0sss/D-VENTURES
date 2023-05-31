import sqlite3 as sq
from database.models.models_main import db
from database.models.class_model import Clas


def get_class_info(class_id):
    with db:
        try:
            cur = db.cursor()
            query = Clas.select().where(Clas.clas_id == class_id)
            cur.execute(str(query))
            records = cur.fetchall()
            return records
        except sq.Error as error:
            print("Error with database", error)


def get_total_classes():
    with db:
        try:
            cur = db.cursor()
            query = Clas.select()
            cur.execute(str(query))
            records = len(cur.fetchall())
            cur.close()
            return records
        except sq.Error as error:
            print("Error with database", error)

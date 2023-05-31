import sqlite3 as sq
from database.models.models_main import db
from database.models.user_model import User

def user_existance_check(user_id):
    with db:
        try:
            cur = db.cursor()
            query = User.select().where(User.user_id == user_id)
            cur.execute(str(query))
            records = cur.fetchall()
            if not records:
                cur.close()
                print(1)
                return False
            else:
                cur.close()
                print(0)
                return True
        except sq.Error as error:
            print("Error with database", error)

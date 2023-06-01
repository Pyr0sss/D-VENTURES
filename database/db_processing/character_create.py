from database.models.character_model import Character

def create_character(id, name, race, clas, origin, level):
    Character.create(user_id=id, name=name, race=race, clas=clas, origin=origin, level=level)
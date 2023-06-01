from database.models.character_model import Character

def update_name(id, name):
    character = Character.get(Character.character_id == id)
    character.name = name
    character.save()

def update_race(id, race):
    character = Character.get(Character.character_id == id)
    character.race = race
    character.save()

def update_class(id, clas):
    character = Character.get(Character.character_id == id)
    character.clas = clas
    character.save()

def update_origin(id, origin):
    character = Character.get(Character.character_id == id)
    character.origin = origin
    character.save()

def update_level(id, level):
    character = Character.get(Character.character_id == id)
    character.level = level
    character.save()
from database.models.character_model import Character

def update_name(id, name):
    character = Character.get(Character.character_id == id)
    character.name = name
    character.save()

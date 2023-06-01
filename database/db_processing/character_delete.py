from database.models.character_model import Character

def del_character(id):
    character = Character.get(Character.character_id == id)
    character.delete_instance()
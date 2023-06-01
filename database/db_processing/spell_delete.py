from database.models.spell_model import Spell

def del_spell(id):
    spell = Spell.get(Spell.spell_id == id)
    spell.delete_instance()
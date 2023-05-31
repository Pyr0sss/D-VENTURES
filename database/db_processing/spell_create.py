from database.models.spell_model import Spell

def class_member(all, now):
    for i in range (len(all)):
        if all[i] in now:
            all[i] = 1
        else:
            all[i] = 0
    return all

def new_spell(name, level, classes, desc):
    all_classes = ["class_wizard", "class_warlock", "class_sorcerer", "class_bard", "class_cleric", "class_druid",
                   "class_paladin", "class_artificer", "class_ranger"]
    classes = list(classes)
    chars = class_member(all_classes, classes)
    Spell.create(spell_name=name, level=level, class_wizard=chars[0], class_warlock=chars[1], class_sorcerer=chars[2],
                 class_bard=chars[3], class_cleric=chars[4], class_druid=chars[5], class_paladin=chars[6],
                 class_artificer=chars[7], class_ranger=chars[8], description=desc)

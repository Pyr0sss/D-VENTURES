from database.db_processing.class_processing import get_total_classes
from database.db_processing.origin_processing import get_total_origins
from database.db_processing.race_processing import get_total_races
from database.db_processing.spell_processing import get_total_spells

race_counter: int
class_counter: int
origin_counter: int
spells_counter: int


def set_counters():
    global race_counter, class_counter, origin_counter, spells_counter
    race_counter = get_total_races()
    class_counter = get_total_classes()
    origin_counter = get_total_origins()
    spells_counter = get_total_spells()

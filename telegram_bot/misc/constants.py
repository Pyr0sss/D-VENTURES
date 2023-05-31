from database.db_processing.class_processing import get_total_classes
from database.db_processing.origin_processing import get_total_origins
from database.db_processing.race_processing import get_total_races

race_counter: int
class_counter: int
origin_counter: int


def set_counters():
    global race_counter, class_counter, origin_counter
    race_counter = get_total_races()
    class_counter = get_total_classes()
    origin_counter = get_total_origins()

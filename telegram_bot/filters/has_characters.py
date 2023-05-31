import typing
from aiogram.dispatcher.filters import BoundFilter
from database.db_processing.character_processing import read_limited_characters_page


class HasCharacterFilter(BoundFilter):
    key = 'has_character'

    def __init__(self, has_character: typing.Optional[bool] = None):
        self.has_character = has_character

    async def check(self, obj):
        records = len(read_limited_characters_page(obj.from_user.id))
        if records == 0:
            return False
        return True

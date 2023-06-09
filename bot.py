import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from telegram_bot.config import load_config
from telegram_bot.filters.admin import AdminFilter
from telegram_bot.filters.has_characters import HasCharacterFilter
from telegram_bot.handlers.admin import register_admin
from telegram_bot.handlers.admin_spell_settings import register_admin_spell_settings
from telegram_bot.handlers.character_creation import register_character_creation
from telegram_bot.handlers.character_editing import register_character_editing
from telegram_bot.handlers.character_selection import register_character_selection
from telegram_bot.handlers.spell_guide import register_spell_guide
from telegram_bot.handlers.user import register_user
from telegram_bot.middlewares.throttling import ThrottlingMiddleware
from telegram_bot.misc.dice_throwing import register_dice
from telegram_bot.misc.constants import set_counters

from telegram_bot.handlers.qualities_calculation import register_qualities

from database.db_processing.db_creation import db_creation

logger = logging.getLogger(__name__)


def register_middlewares(dp):
    dp.setup_middleware(ThrottlingMiddleware())


def register_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(HasCharacterFilter)


def register_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_character_creation(dp)
    register_character_editing(dp)
    register_character_selection(dp)
    register_spell_guide(dp)
    register_admin_spell_settings(dp)
    register_dice(dp)
    register_qualities(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )

    storage = MemoryStorage()
    config = load_config(".env")
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config
    register_middlewares(dp)
    register_filters(dp)
    register_handlers(dp)
    db_creation()
    set_counters()
    #spells()
    #races()
    #origins()
    #classes()

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot has stopped it's work!")

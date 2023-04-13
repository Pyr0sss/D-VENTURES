import asyncio
import logging

from aiogram import Bot, Dispatcher

from telegram_bot.config import load_config
from telegram_bot.filters.admin import AdminFilter
from telegram_bot.handlers.admin import register_admin
from telegram_bot.handlers.echo import register_echo
from telegram_bot.handlers.user import register_user

logger = logging.getLogger(__name__)


def register_middlewares(dp):
    #dp.setup_middleware(...)
    pass


def register_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_handlers(dp):
    #register_admin(dp)
    register_user(dp)
    register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    config = load_config(".env")
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(bot)
    bot['config'] = config
    register_middlewares(dp)
    register_filters(dp)
    register_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await bot.get_session()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot has stopped it's work!")

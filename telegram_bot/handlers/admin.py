from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from telegram_bot.keyboards.reply import main_menu
from telegram_bot.keyboards.reply_keyboards.admin_keyboard import admin_panel


async def admin_start(message: types.Message):
    await message.answer('Админ-панель доступна!', reply_markup=admin_panel)


async def return_to_bot(message: types.Message):
    await message.answer('Режим обычного пользователя активирован. Для активации панели админа используйте команду'
                         ' `/commands`', reply_markup=main_menu, parse_mode='Markdown')


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=['start'], is_admin=True)
    dp.register_message_handler(admin_start, commands=['commands'], is_admin=True)
    dp.register_message_handler(return_to_bot, Text(equals='Вернуться к основному функционалу', ignore_case=True),
                                is_admin=True)

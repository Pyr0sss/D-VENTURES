import logging

from aiogram import types, Dispatcher

from telegram_bot.keyboards.reply import main_menu


async def admin_start(message: types.Message):
    await message.reply('Hello, Admin!', reply_markup=main_menu)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=['start'], is_admin=True)

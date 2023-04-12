from aiogram import types, Dispatcher


async def admin_start(message: types.Message):
    await message.reply('Hello, Admin!')


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=['start'], is_admin=True)

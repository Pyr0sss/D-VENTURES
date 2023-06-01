from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from database.models.qualities_model import Quality
from telegram_bot.misc.dice_throwing import throw_dice_20

async def calculate_qualities(message: types.Message, state=FSMContext):
    await message.answer("Доверимся проведению!")
    async with state.proxy() as data:
        data["force"] = await throw_dice_20(message)
    await message.answer("Запишем это значение в ваш уровень силы. Продолжаем!")
    async with state.proxy() as data:
        data["agility"] = await throw_dice_20(message)
    await message.answer("А это теперь ваша ловкость! Перейдем к телосложению.")
    async with state.proxy() as data:
        data["body"] = await throw_dice_20(message)
    await message.answer("Феноменально! А что насчет интеллекта?")
    async with state.proxy() as data:
        data["intellect"] = await throw_dice_20(message)
    await message.answer("Отличный результат! Переходим к мудрости.")
    async with state.proxy() as data:
        data["wisdom"] = await throw_dice_20(message)
    await message.answer("Осталась только харизма!")
    async with state.proxy() as data:
        data["charisma"] = await throw_dice_20(message)
    async with state.proxy() as data:
        Quality.create(user_id=message.from_user.id, character_id=1, force=data["force"], agility=data["agility"],
                       body=data["body"], intellect=data["intellect"], wisdom=data['wisdom'], charisma=data["charisma"])


def register_quilities(dp: Dispatcher):
    dp.register_message_handler(calculate_qualities, state='*', commands="test")
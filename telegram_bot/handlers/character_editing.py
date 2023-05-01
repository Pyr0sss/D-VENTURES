from aiogram.types import CallbackQuery

from database.db_sqlite3 import db_insert
from telegram_bot.keyboards.callback_datas import confirmation_callback, character_edit_callback
from telegram_bot.keyboards.inline import confirmation_menu, character_info
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram_bot.keyboards.reply import main_menu


class FSMCharacter(StatesGroup):
    confirmation = State()
    editing = State()
    edit_name = State()
    edit_race = State()
    edit_clas = State()
    edit_origin = State()
    edit_level = State()


async def edit_character(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await FSMCharacter.editing.set()
    await call.message.answer("Оу, видимо я так увлекся твоим рассказом, что допустил ошибку в своих заметках..."
                              " Не мог бы ты уточнить, что я прослушал?", reply_markup=character_info)


async def edit_name(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введи свое новое имя")
    await FSMCharacter.edit_name.set()


async def set_new_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMCharacter.confirmation.set()
    await message.answer(f'Дай-ка запишу о тебе в своем блокноте\n\n-------------------\n'
                         f'🔅 Персонаж: {data["name"]} (уровень: {data["level"]})\n'
                         f'🧑‍🦳 Раса: {data["race"]}\n🧙 Класс: {data["clas"]}\n👼 Происхождение: {data["origin"]}\n-------------------\n'
                         f'\nПроверь меня, я все правильно услышал?', reply_markup=confirmation_menu)


async def edit_race(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введи свою новую расу")
    await FSMCharacter.edit_race.set()


async def set_new_race(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['race'] = message.text
    await FSMCharacter.confirmation.set()
    await message.answer(f'Дай-ка запишу о тебе в своем блокноте\n\n-------------------\n'
                         f'🔅 Персонаж: {data["name"]} (уровень: {data["level"]})\n'
                         f'🧑‍🦳 Раса: {data["race"]}\n🧙 Класс: {data["clas"]}\n👼 Происхождение: {data["origin"]}\n-------------------\n'
                         f'\nПроверь меня, я все правильно услышал?', reply_markup=confirmation_menu)


async def edit_clas(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введи свой новый класс")
    await FSMCharacter.edit_clas.set()


async def set_new_clas(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['clas'] = message.text
    await FSMCharacter.confirmation.set()
    await message.answer(f'Дай-ка запишу о тебе в своем блокноте\n\n-------------------\n'
                         f'🔅 Персонаж: {data["name"]} (уровень: {data["level"]})\n'
                         f'🧑‍🦳 Раса: {data["race"]}\n🧙 Класс: {data["clas"]}\n👼 Происхождение: {data["origin"]}\n-------------------\n'
                         f'\nПроверь меня, я все правильно услышал?', reply_markup=confirmation_menu)


async def edit_origin(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введи свою новую расу")
    await FSMCharacter.edit_origin.set()


async def set_new_origin(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['origin'] = message.text
    await FSMCharacter.confirmation.set()
    await message.answer(f'Дай-ка запишу о тебе в своем блокноте\n\n-------------------\n'
                         f'🔅 Персонаж: {data["name"]} (уровень: {data["level"]})\n'
                         f'🧑‍🦳 Раса: {data["race"]}\n🧙 Класс: {data["clas"]}\n👼 Происхождение: {data["origin"]}\n-------------------\n'
                         f'\nПроверь меня, я все правильно услышал?', reply_markup=confirmation_menu)


async def edit_level(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введи свой уровень")
    await FSMCharacter.edit_level.set()


async def set_new_level(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['level'] = int(message.text)
    await FSMCharacter.confirmation.set()
    await message.answer(f'Дай-ка запишу о тебе в своем блокноте\n\n-------------------\n'
                         f'🔅 Персонаж: {data["name"]} (уровень: {data["level"]})\n'
                         f'🧑‍🦳 Раса: {data["race"]}\n🧙 Класс: {data["clas"]}\n👼 Происхождение: {data["origin"]}\n-------------------\n'
                         f'\nПроверь меня, я все правильно услышал?', reply_markup=confirmation_menu)


def register_character_editing(dp: Dispatcher):
    dp.register_callback_query_handler(edit_character, confirmation_callback.filter(choice="no"),
                                       state=FSMCharacter.confirmation)
    dp.register_callback_query_handler(edit_name, character_edit_callback.filter(info="name"),
                                       state=FSMCharacter.editing)
    dp.register_callback_query_handler(edit_race, character_edit_callback.filter(info="race"),
                                       state=FSMCharacter.editing)
    dp.register_callback_query_handler(edit_clas, character_edit_callback.filter(info="clas"),
                                       state=FSMCharacter.editing)
    dp.register_callback_query_handler(edit_origin, character_edit_callback.filter(info="origin"),
                                       state=FSMCharacter.editing)
    dp.register_callback_query_handler(edit_level, character_edit_callback.filter(info="level"),
                                       state=FSMCharacter.editing)
    dp.register_message_handler(set_new_name, state=FSMCharacter.edit_name)
    dp.register_message_handler(set_new_race, state=FSMCharacter.edit_race)
    dp.register_message_handler(set_new_clas, state=FSMCharacter.edit_clas)
    dp.register_message_handler(set_new_origin, state=FSMCharacter.edit_origin)
    dp.register_message_handler(set_new_level, state=FSMCharacter.edit_level)

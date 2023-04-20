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
    name = State()
    race = State()
    clas = State()
    origin = State()
    level = State()
    confirmation = State()
    editing = State()
    edit_name = State()
    edit_race = State()
    edit_clas = State()
    edit_origin = State()
    edit_level = State()


async def create_character(message: types.Message, state=FSMContext):
    await FSMCharacter.name.set()
    async with state.proxy() as data:
        data['user_id'] = int(message.from_user.id)
    await message.reply('Как зовут тебя, путник?')


async def set_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMCharacter.next()
    await message.reply(f'Что-то мне подсказывает, что происходит рождение нового героя - {data["name"]}, '
                        f'о ком барды будут складывать песни. А какие песни, решать уже тебе!\nВыбери расу будущего персонажа')


async def set_race(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['race'] = message.text
    await FSMCharacter.next()
    await message.reply(f'{data["race"]} - отличный выбор! Теперь расскажи, какой класс ты выбрал для своих странствий')


async def set_clas(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['clas'] = message.text
    await FSMCharacter.next()
    await message.reply(
        f'Хмм, {data["clas"]}... У него есть достойная история? Поведай ее или же выбери одно из предложенных сказаний')


async def set_origin(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['origin'] = message.text
    await FSMCharacter.next()
    await message.reply(f'История от {data["origin"]} я еще не слыхал. Теперь скажи, какого уровня ты смог достичь?')


async def set_level(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['level'] = int(message.text)
    await FSMCharacter.next()
    await message.answer(f'Дай-ка запишу о тебе в своем блокноте\n\n-------------------\n'
                         f'🔅 Персонаж: {data["name"]} (уровень: {data["level"]})\n'
                         f'🧑‍🦳 Раса: {data["race"]}\n🧙 Класс: {data["clas"]}\n👼 Происхождение: {data["origin"]}\n-------------------\n'
                         f'\nПроверь меня, я все правильно услышал?', reply_markup=confirmation_menu)


async def save_character(call: types.CallbackQuery, state=FSMContext):
    await call.answer(cache_time=60)
    await db_insert(state)
    await state.finish()
    await call.message.answer("Твоя история невероятна! Спасибо, что поделился ею со мной!")
    await call.message.edit_reply_markup(reply_markup=None)


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


async def stop_creating_character(message: types.Message, state=FSMContext):
    await state.finish()
    await message.answer("Видимо сейчас ты не готов со своей историей... Не переживай, я всегда буду здесь, чтобы"
                         " послушать о твоих приключениях!", reply_markup=main_menu)


def register_character_creation(dp: Dispatcher):
    dp.register_callback_query_handler(save_character, confirmation_callback.filter(choice="yes"),
                                       state=FSMCharacter.confirmation)
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

    dp.register_message_handler(create_character, Text(equals='Создать персонажа', ignore_case=True), state=None)
    dp.register_message_handler(stop_creating_character, Text(equals='Отменить создание персонажа', ignore_case=True),
                                state=FSMCharacter.all_states)
    dp.register_message_handler(set_name, state=FSMCharacter.name)
    dp.register_message_handler(set_race, state=FSMCharacter.race)
    dp.register_message_handler(set_clas, state=FSMCharacter.clas)
    dp.register_message_handler(set_origin, state=FSMCharacter.origin)
    dp.register_message_handler(set_level, state=FSMCharacter.level)
    dp.register_message_handler(set_new_name, state=FSMCharacter.edit_name)
    dp.register_message_handler(set_new_race, state=FSMCharacter.edit_race)
    dp.register_message_handler(set_new_clas, state=FSMCharacter.edit_clas)
    dp.register_message_handler(set_new_origin, state=FSMCharacter.edit_origin)
    dp.register_message_handler(set_new_level, state=FSMCharacter.edit_level)

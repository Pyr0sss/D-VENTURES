from aiogram.types import CallbackQuery

from database.db_sqlite3 import db_insert
from telegram_bot.keyboards.callback_datas import confirmation_callback
from telegram_bot.keyboards.inline import confirmation_menu
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram_bot.keyboards.reply import blank, main_menu


class FSMCharacter(StatesGroup):
    name = State()
    race = State()
    clas = State()
    origin = State()
    level = State()
    confirmation = State()


async def create_character(message: types.Message, state=FSMContext):
    await FSMCharacter.name.set()
    async with state.proxy() as data:
        data['user_id'] = int(message.from_user.id)
    await message.reply('Как зовут тебя, путник?', reply_markup=blank)


async def set_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMCharacter.next()
    await message.reply(f'Что-то мне подсказывает, что происходит рождение нового героя - {data["name"]}, '
                        f'о ком барды будут складывать песни. А какие песни, решать уже тебе!\nВыбери расу будущего персонажа',
                        reply_markup=blank)


async def set_race(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['race'] = message.text
    await FSMCharacter.next()
    await message.reply(f'{data["race"]} - отличный выбор! Теперь расскажи, какой класс ты выбрал для своих странствий',
                        reply_markup=blank)


async def set_clas(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['clas'] = message.text
    await FSMCharacter.next()
    await message.reply(
        f'Хмм, {data["clas"]}... У него есть достойная история? Поведай ее или же выбери одно из предложенных сказаний',
        reply_markup=blank)


async def set_origin(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['origin'] = message.text
    await FSMCharacter.next()
    await message.reply(f'История от {data["origin"]} я еще не слыхал. Теперь скажи, какого уровня ты смог достичь?',
                        reply_markup=blank)


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


async def stop_creating_character(message: types.Message, state=FSMContext):
    await state.finish()
    await message.answer("Видимо сейчас ты не готов со своей историей... Не переживай, я всегда буду здесь, чтобы"
                         " послушать о твоих приключениях!", reply_markup=main_menu)


def register_character_creation(dp: Dispatcher):
    dp.register_callback_query_handler(save_character, confirmation_callback.filter(choice="yes"),
                                       state=FSMCharacter.confirmation)
    dp.register_message_handler(create_character, Text(equals='Создать персонажа', ignore_case=True), state=None)
    dp.register_message_handler(stop_creating_character, Text(equals='Отменить создание персонажа', ignore_case=True),
                                state=FSMCharacter.all_states)
    dp.register_message_handler(set_name, state=FSMCharacter.name)
    dp.register_message_handler(set_race, state=FSMCharacter.race)
    dp.register_message_handler(set_clas, state=FSMCharacter.clas)
    dp.register_message_handler(set_origin, state=FSMCharacter.origin)
    dp.register_message_handler(set_level, state=FSMCharacter.level)

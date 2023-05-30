from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from database.db_sqlite3 import db_insert
from telegram_bot.keyboards.reply import ready, main_menu


class FSMCharacter(StatesGroup):
    name = State()
    race = State()
    clas = State()
    origin = State()
    level = State()


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
    await message.reply(f'Хмм, {data["clas"]}... У него есть достойная история? Поведай ее или же выбери одно из предложенных сказаний')


async def set_origin(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['origin'] = message.text
    await FSMCharacter.next()
    await message.reply(f'История от {data["origin"]} я еще не слыхал. Теперь скажи, какого уровня ты смог достичь?')


async def set_level(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['level'] = int(message.text)

    #необходимо сделать подтвержение правильности введения данных
    await db_insert(state)
    await state.finish()

    await message.answer(f'Дай-ка запишу о тебе в своем блокноте\n\n-------------------\n'
                                       f'🔅 Персонаж: {data["name"]} (уровень: {data["level"]})\n'
        f'🧑‍🦳 Раса: {data["race"]}\n🧙 Класс: {data["clas"]}\n👼 Происхождение: {data["origin"]}\n-------------------\n'
        f'\nПроверь меня, я все правильно услышал?')



async def user_welcome(message: types.Message):
    text = "Здравствуй, дорогой путешественник! Добро пожаловать в D&VENTURES! " \
           "Готов ли ты полностью погрузиться в захватывающее приключение? " \
           "Если так, то этот бот поможет сделать его еще более увлекательным и незабываемым!\nГотов к бою?"
    await message.answer(text, reply_markup=ready)


async def user_main_menu(message: types.Message):
    text = "Здравствуй, таинственный незнакомец! Присядь, выпей бренди на дорожку и поведай мне кто ты таков? " \
           "Ежели твоя волшебная идентичность еще не определена, то советую заглянуть в древний магический справочник" \
           " – он поможет с выбором и поведает тебе обо всем на свете."
    await message.answer(text, reply_markup=main_menu)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_welcome, commands=['start'])
    dp.register_message_handler(user_main_menu, Text(equals='В бой! 🏹', ignore_case=True), state='*')
    dp.register_message_handler(create_character, Text(equals='Создать персонажа 📮', ignore_case=True), state=None)
    dp.register_message_handler(set_name, state=FSMCharacter.name)
    dp.register_message_handler(set_race, state=FSMCharacter.race)
    dp.register_message_handler(set_clas, state=FSMCharacter.clas)
    dp.register_message_handler(set_origin, state=FSMCharacter.origin)
    dp.register_message_handler(set_level, state=FSMCharacter.level)

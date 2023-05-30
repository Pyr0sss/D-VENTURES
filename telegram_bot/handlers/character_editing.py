from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from telegram_bot.handlers.character_creation import races, classes
from telegram_bot.keyboards.callback_datas import confirmation_callback, character_edit_callback, \
    character_creation_callback, page_button_callback
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
    await FSMCharacter.edit_race.set()

    button_list = []
    for i in range(0, 6, 2):
        button_list.append([InlineKeyboardButton(text=races[i], callback_data=character_creation_callback.new(
            action="race", race=races[i][:-2], clas="null")), InlineKeyboardButton(text=races[i + 1],
                                                                                   callback_data=character_creation_callback.new(
                                                                                       action="race",
                                                                                       race=races[i + 1][:-2],
                                                                                       clas="null"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page="1", action="prev")),
        InlineKeyboardButton(text="1", callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page="1", action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.answer('Выбери свою новую расу', reply_markup=markup)


async def set_new_race(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    race = callback_data.get("race")
    async with state.proxy() as data:
        data['race'] = race
    await call.message.edit_reply_markup(reply_markup=None)
    await FSMCharacter.confirmation.set()
    await call.message.edit_text(f'Дай-ка запишу о тебе в своем блокноте\n\n-------------------\n'
                         f'🔅 Персонаж: {data["name"]} (уровень: {data["level"]})\n'
                         f'🧑‍🦳 Раса: {data["race"]}\n🧙 Класс: {data["clas"]}\n👼 Происхождение: {data["origin"]}\n-------------------\n'
                         f'\nПроверь меня, я все правильно услышал?', reply_markup=confirmation_menu)


async def next_page_race(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    data = int(callback_data.get("page")) + 1

    if data > len(races) / 6 + 1:
        return

    button_list = []
    for i in range((data - 1) * 6, data * 6, 2):

        if i >= len(races):
            break

        button_list.append([InlineKeyboardButton(text=races[i], callback_data=character_creation_callback.new(
            action="race", race=races[i][:-2], clas="null")), InlineKeyboardButton(text=races[i + 1],
                                                                                   callback_data=character_creation_callback.new(
                                                                                       action="race",
                                                                                       race=races[i + 1][:-2],
                                                                                       clas="null"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev")),
        InlineKeyboardButton(text=str(data), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.edit_reply_markup(markup)


async def prev_page_race(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    data = int(callback_data.get("page")) - 1

    if data < 1:
        return

    button_list = []
    for i in range((data - 1) * 6, data * 6, 2):

        if i >= len(races):
            break

        button_list.append([InlineKeyboardButton(text=races[i], callback_data=character_creation_callback.new(
            action="race", race=races[i][:-2], clas="null")), InlineKeyboardButton(text=races[i + 1],
                                                                                   callback_data=character_creation_callback.new(
                                                                                       action="race",
                                                                                       race=races[i + 1][:-2],
                                                                                       clas="null"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev")),
        InlineKeyboardButton(text=str(data), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.edit_reply_markup(markup)


async def edit_clas(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await FSMCharacter.edit_clas.set()

    button_list = []
    for i in range(3):
        button_list.append([InlineKeyboardButton(text=classes[i], callback_data=character_creation_callback.new(
            action="clas", race="null", clas=classes[i][:-2]))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page="1", action="prev")),
        InlineKeyboardButton(text="1", callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page="1", action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.answer("Теперь выбери свой новый класс!", reply_markup=markup)


async def set_new_clas(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    clas = callback_data.get("clas")
    async with state.proxy() as data:
        data['clas'] = clas
    await FSMCharacter.confirmation.set()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.edit_text(f'Дай-ка запишу о тебе в своем блокноте\n\n-------------------\n'
                         f'🔅 Персонаж: {data["name"]} (уровень: {data["level"]})\n'
                         f'🧑‍🦳 Раса: {data["race"]}\n🧙 Класс: {data["clas"]}\n👼 Происхождение: {data["origin"]}\n-------------------\n'
                         f'\nПроверь меня, я все правильно услышал?', reply_markup=confirmation_menu)


async def next_page_class(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    data = int(callback_data.get("page")) + 1

    if data > len(classes) / 3 + 1:
        return

    button_list = []
    for i in range((data - 1) * 3, data * 3):

        if i >= len(classes):
            break

        button_list.append([InlineKeyboardButton(text=classes[i], callback_data=character_creation_callback.new(
            action="clas", race="null", clas=classes[i][:-2]))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev")),
        InlineKeyboardButton(text=str(data), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.edit_reply_markup(markup)


async def prev_page_class(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    data = int(callback_data.get("page")) - 1

    if data < 1:
        return

    button_list = []
    for i in range((data - 1) * 3, data * 3):

        if i >= len(classes):
            break

        button_list.append([InlineKeyboardButton(text=classes[i], callback_data=character_creation_callback.new(
            action="clas", race="null", clas=classes[i][:-2]))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev")),
        InlineKeyboardButton(text=str(data), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.edit_reply_markup(markup)


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
    try:
        async with state.proxy() as data:
            data['level'] = int(message.text)
        await FSMCharacter.confirmation.set()
        await message.answer(f'Дай-ка запишу о тебе в своем блокноте\n\n-------------------\n'
                             f'🔅 Персонаж: {data["name"]} (уровень: {data["level"]})\n'
                             f'🧑‍🦳 Раса: {data["race"]}\n🧙 Класс: {data["clas"]}\n👼 Происхождение: {data["origin"]}\n-------------------\n'
                             f'\nПроверь меня, я все правильно услышал?', reply_markup=confirmation_menu)
    except:
        await message.answer("Вот это да! Не знаю, как у вас, но у нас мастерство показывается с помощью числа. "
                             "Попробуй дать оценку своего уровня в виде числа!")


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
    # dp.register_message_handler(set_new_race, state=FSMCharacter.edit_race)
    # dp.register_message_handler(set_new_clas, state=FSMCharacter.edit_clas)
    dp.register_message_handler(set_new_origin, state=FSMCharacter.edit_origin)
    dp.register_message_handler(set_new_level, state=FSMCharacter.edit_level)

    dp.register_callback_query_handler(next_page_race, page_button_callback.filter(action="next"),
                                       state=FSMCharacter.edit_race)
    dp.register_callback_query_handler(prev_page_race, page_button_callback.filter(action="prev"),
                                       state=FSMCharacter.edit_race)
    dp.register_callback_query_handler(set_new_race, character_creation_callback.filter(action="race"),
                                       state=FSMCharacter.edit_race)
    dp.register_callback_query_handler(next_page_class, page_button_callback.filter(action="next"),
                                       state=FSMCharacter.edit_clas)
    dp.register_callback_query_handler(prev_page_class, page_button_callback.filter(action="prev"),
                                       state=FSMCharacter.edit_clas)
    dp.register_callback_query_handler(set_new_clas, character_creation_callback.filter(action="clas"),
                                       state=FSMCharacter.edit_clas)

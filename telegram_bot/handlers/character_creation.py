from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from database.db_processing.class_processing import get_class_info
from database.db_processing.origin_processing import get_origin_info
from database.db_processing.race_processing import get_race_info, get_total_races
from database.models.character_model import Character

from telegram_bot.keyboards.callback_datas import confirmation_callback, character_edit_callback, \
    character_creation_callback, page_button_callback, creation_confirmation_callback
from telegram_bot.keyboards.inline import confirmation_menu, character_info, cancel_menu
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram_bot.keyboards.reply import main_menu
from telegram_bot.misc import constants


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
        data['player_id'] = id
    async with state.proxy() as data:
        data['user_id'] = int(message.from_user.id)
    await message.reply('Как зовут тебя, путник?', reply_markup=cancel_menu)


async def set_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMCharacter.next()
    await message.reply(f'Что-то мне подсказывает, что происходит рождение нового героя - {data["name"]}, '
                        f'о ком барды будут складывать песни. А какие песни, решать уже тебе!')
    button_list = []
    for i in range(1, 7, 2):
        button_list.append([InlineKeyboardButton(text=str(get_race_info(i)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i, type="race")),
                            InlineKeyboardButton(text=str(get_race_info(i + 1)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i + 1,
                                                                                               type="race"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page="1", action="prev")),
        InlineKeyboardButton(text="1", callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page="1", action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await message.answer('Выбери свою расу', reply_markup=markup)


async def show_race_list(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    button_list = []
    for i in range(1, 7, 2):
        button_list.append([InlineKeyboardButton(text=str(get_race_info(i)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i, type="race")),
                            InlineKeyboardButton(text=str(get_race_info(i + 1)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i + 1,
                                                                                               type="race"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page="1", action="prev")),
        InlineKeyboardButton(text="1", callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page="1", action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.answer('Выбери свою расу', reply_markup=markup)


async def next_page_race(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    data = int(callback_data.get("page")) + 1

    if data >= constants.race_counter / 6 + 1:
        return

    button_list = []
    for i in range((data - 1) * 6 + 1, data * 6 + 1, 2):

        if i > constants.race_counter:
            break

        button_list.append([InlineKeyboardButton(text=str(get_race_info(i)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i, type="race")),
                            InlineKeyboardButton(text=str(get_race_info(i + 1)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i + 1,
                                                                                               type="race"))])

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
    for i in range((data - 1) * 6 + 1, data * 6 + 1, 2):

        if i >= constants.race_counter:
            break

        button_list.append([InlineKeyboardButton(text=str(get_race_info(i)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i, type="race")),
                            InlineKeyboardButton(text=str(get_race_info(i + 1)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i + 1,
                                                                                               type="race"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev")),
        InlineKeyboardButton(text=str(data), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.edit_reply_markup(markup)


async def set_race_info(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    race = callback_data.get("info")
    race_info = get_race_info(race)[0]
    await call.message.answer(race_info[1] + " : " + race_info[2])
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="Нет", callback_data=creation_confirmation_callback.new(choice="no", info=race)),
        InlineKeyboardButton(text="Да", callback_data=creation_confirmation_callback.new(choice="yes", info=race)),
    )
    await call.message.answer("Ты уверен, что хочешь выбрать эту расу?", reply_markup=markup)


async def set_race(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()

    race = callback_data.get("info")
    async with state.proxy() as data:
        data['race'] = get_race_info(race)[0][1]
    await FSMCharacter.next()
    await call.message.edit_reply_markup(reply_markup=None)

    button_list = []
    for i in range(1, 4):
        button_list.append([InlineKeyboardButton(text=str(get_class_info(i)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i, type="class"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page="1", action="prev")),
        InlineKeyboardButton(text="1", callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page="1", action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.edit_text(f'{data["race"]} - отличный выбор! Теперь расскажи, какой класс ты'
                                 f' выбрал для своих странствий')
    await call.message.answer("Теперь выбери свой класс!", reply_markup=markup)


async def next_page_class(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    data = int(callback_data.get("page")) + 1

    if data >= constants.class_counter / 3 + 1:
        return

    button_list = []
    for i in range((data - 1) * 3 + 1, data * 3 + 1):

        if i > constants.class_counter:
            break

        button_list.append([InlineKeyboardButton(text=str(get_class_info(i)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i, type="class"))])

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
    for i in range((data - 1) * 3 + 1, data * 3 + 1):

        if i > constants.class_counter:
            break

        button_list.append([InlineKeyboardButton(text=str(get_class_info(i)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i, type="class"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev")),
        InlineKeyboardButton(text=str(data), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.edit_reply_markup(markup)


async def show_class_list(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    button_list = []
    for i in range(1, 4):
        button_list.append([InlineKeyboardButton(text=str(get_class_info(i)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i, type="class"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page="1", action="prev")),
        InlineKeyboardButton(text="1", callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page="1", action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.answer('Выбери свой класс', reply_markup=markup)


async def set_class_info(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    clas = callback_data.get("info")
    clas_info = get_class_info(clas)[0]
    await call.message.answer(clas_info[1] + " : " + clas_info[2])
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="Нет", callback_data=creation_confirmation_callback.new(choice="no", info=clas)),
        InlineKeyboardButton(text="Да", callback_data=creation_confirmation_callback.new(choice="yes", info=clas)),
    )
    await call.message.answer("Ты уверен, что хочешь выбрать этот класс?", reply_markup=markup)


async def set_clas(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    clas = callback_data.get("info")
    async with state.proxy() as data:
        data['clas'] = get_class_info(clas)[0][1]
    await FSMCharacter.next()
    await call.message.edit_reply_markup(reply_markup=None)

    button_list = []
    for i in range(1, 4):
        button_list.append([InlineKeyboardButton(text=str(get_origin_info(i)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i, type="origin"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page="1", action="prev")),
        InlineKeyboardButton(text="1", callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page="1", action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.answer(
        f'Хмм, {data["clas"]}... У него есть достойная история? Поведай ее или же выбери одно из предложенных сказаний',
        reply_markup=markup)


async def next_page_origin(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    data = int(callback_data.get("page")) + 1

    if data >= constants.origin_counter / 3 + 1:
        return

    button_list = []
    for i in range((data - 1) * 3 + 1, data * 3 + 1):

        if i > constants.origin_counter:
            break

        button_list.append([InlineKeyboardButton(text=str(get_origin_info(i)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i, type="origin"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev")),
        InlineKeyboardButton(text=str(data), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.edit_reply_markup(markup)


async def prev_page_origin(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    data = int(callback_data.get("page")) - 1

    if data < 1:
        return

    button_list = []
    for i in range((data - 1) * 3 + 1, data * 3 + 1):

        if i > constants.origin_counter:
            break

        button_list.append([InlineKeyboardButton(text=str(get_origin_info(i)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i, type="origin"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev")),
        InlineKeyboardButton(text=str(data), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.edit_reply_markup(markup)


async def show_origin_list(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    button_list = []
    for i in range(1, 4):
        button_list.append([InlineKeyboardButton(text=str(get_origin_info(i)[0][1]),
                                                 callback_data=character_creation_callback.new(info=i, type="origin"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page="1", action="prev")),
        InlineKeyboardButton(text="1", callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page="1", action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.answer('Выбери своё происхождение', reply_markup=markup)


async def set_origin_info(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    origin = callback_data.get("info")
    origin_info = get_origin_info(origin)[0]
    await call.message.answer(origin_info[1] + " : " + origin_info[2])
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="Нет", callback_data=creation_confirmation_callback.new(choice="no", info=origin)),
        InlineKeyboardButton(text="Да", callback_data=creation_confirmation_callback.new(choice="yes", info=origin)),
    )
    await call.message.answer("Ты уверен, что хочешь выбрать это происхождение?", reply_markup=markup)


async def set_origin(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    origin = callback_data.get("info")
    async with state.proxy() as data:
        data['origin'] = get_origin_info(origin)[0][1]
    await FSMCharacter.next()
    await call.message.reply(
        f'История от {data["origin"]} я еще не слыхал. Теперь скажи, какого уровня ты смог достичь?',
        reply_markup=cancel_menu)


async def set_level(message: types.Message, state=FSMContext):
    try:
        async with state.proxy() as data:
            data['level'] = int(message.text)
        await FSMCharacter.next()
        await message.answer(f'Дай-ка запишу о тебе в своем блокноте\n\n-------------------\n'
                             f'🔅 Персонаж: {data["name"]} (уровень: {data["level"]})\n'
                             f'🧑‍🦳 Раса: {data["race"]}\n🧙 Класс: {data["clas"]}\n👼 Происхождение: {data["origin"]}\n-------------------\n'
                             f'\nТвоя история невероятна! Спасибо, что поделился ею со мной!', reply_markup=main_menu)
        await message.answer('Если ты вдруг запамятовал, то ты можешь вспомнить через `Выбрать персонажа`',
                             parse_mode='Markdown')
        async with state.proxy() as data:
            Character.create(user_id=data["user_id"], name=data["name"], race=data["race"], clas=data["clas"],
                             origin=data["origin"], level=data["level"])
        await state.finish()

    except Exception:
        await message.answer("Вот это да! Не знаю, как у вас, но у нас мастерство показывается с помощью числа. "
                             "Попробуй дать оценку своего уровня в виде числа!")
        print(Exception)


async def stop_creating_character(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(
        "Видимо сейчас ты не готов поделиться своей историей... Не переживай, я всегда буду здесь, чтобы"
        " послушать о твоих приключениях!", reply_markup=main_menu)


def register_character_creation(dp: Dispatcher):
    dp.register_message_handler(create_character, Text(equals='Создать персонажа', ignore_case=True), state="*")
    dp.register_message_handler(stop_creating_character, Text(equals='Отменить создание персонажа', ignore_case=True),
                                state=FSMCharacter.all_states)
    dp.register_message_handler(set_name, state=FSMCharacter.name)
    # dp.register_message_handler(set_race, state=FSMCharacter.race)
    # dp.register_message_handler(set_clas, state=FSMCharacter.clas)
    dp.register_message_handler(set_origin, state=FSMCharacter.origin)
    dp.register_message_handler(set_level, state=FSMCharacter.level)

    dp.register_callback_query_handler(stop_creating_character, confirmation_callback.filter(choice="cancel"),
                                       state=FSMCharacter.all_states)

    # перелистывание страниц
    dp.register_callback_query_handler(next_page_race, page_button_callback.filter(action="next"),
                                       state=FSMCharacter.race)
    dp.register_callback_query_handler(prev_page_race, page_button_callback.filter(action="prev"),
                                       state=FSMCharacter.race)
    dp.register_callback_query_handler(next_page_class, page_button_callback.filter(action="next"),
                                       state=FSMCharacter.clas)
    dp.register_callback_query_handler(prev_page_class, page_button_callback.filter(action="prev"),
                                       state=FSMCharacter.clas)
    dp.register_callback_query_handler(next_page_origin, page_button_callback.filter(action="next"),
                                       state=FSMCharacter.origin)
    dp.register_callback_query_handler(prev_page_origin, page_button_callback.filter(action="prev"),
                                       state=FSMCharacter.origin)

    # подробная информация страниц
    dp.register_callback_query_handler(set_race_info, character_creation_callback.filter(type="race"),
                                       state=FSMCharacter.race)
    dp.register_callback_query_handler(set_class_info, character_creation_callback.filter(type="class"),
                                       state=FSMCharacter.clas)
    dp.register_callback_query_handler(set_origin_info, character_creation_callback.filter(type="origin"),
                                       state=FSMCharacter.origin)

    # повторный выбор
    dp.register_callback_query_handler(show_race_list, creation_confirmation_callback.filter(choice="no"),
                                       state=FSMCharacter.race)
    dp.register_callback_query_handler(show_class_list, creation_confirmation_callback.filter(choice="no"),
                                       state=FSMCharacter.clas)
    dp.register_callback_query_handler(show_origin_list, creation_confirmation_callback.filter(choice="no"),
                                       state=FSMCharacter.origin)

    # переход к следующему шагу
    dp.register_callback_query_handler(set_race, creation_confirmation_callback.filter(choice="yes"),
                                       state=FSMCharacter.race)
    dp.register_callback_query_handler(set_clas, creation_confirmation_callback.filter(choice="yes"),
                                       state=FSMCharacter.clas)
    dp.register_callback_query_handler(set_origin, creation_confirmation_callback.filter(choice="yes"),
                                       state=FSMCharacter.origin)

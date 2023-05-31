from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from database.db_processing.class_processing import get_class_info
from database.db_processing.origin_processing import get_origin_info
from database.db_processing.race_processing import get_race_info
from telegram_bot.handlers.character_selection import show_selected_character_info
from telegram_bot.keyboards.callback_datas import confirmation_callback, character_edit_callback, \
    character_creation_callback, page_button_callback, creation_confirmation_callback, character_settings_callback, \
    character_select_callback
from telegram_bot.keyboards.inline import confirmation_menu, character_info
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram_bot.keyboards.reply import main_menu
from telegram_bot.misc import constants

from database.db_processing.character_update import update_name, update_race, update_class, update_origin, update_level


class FSMCharacter(StatesGroup):
    edit = State()
    edit_name = State()
    edit_race = State()
    edit_class = State()
    edit_origin = State()
    edit_level = State()


async def edit_character(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Что же ты захотел изменить?", reply_markup=character_info)
    await FSMCharacter.edit.set()
    async with state.proxy() as data:
        data['id'] = callback_data.get("id")
        data['num'] = callback_data.get("num")


async def edit_name(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введи свое новое имя")
    await FSMCharacter.edit_name.set()


async def set_new_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        print("name" + data["id"])
    update_name(data["id"], message.text)
    # edit character name = message.txt
    await message.answer("Новое имя - " + message.text + ", установлено!", reply_markup=main_menu)
    await state.finish()


async def edit_race(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await FSMCharacter.edit_race.set()

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


async def set_new_race(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    async with state.proxy() as data:
        print("race" + data["id"])
    race = callback_data.get("info")
    char_id = data["id"]
    num = data["num"]
    update_race(char_id, get_race_info(race)[0][1])
    # edit character race = get_race_info(race)[0][1]
    await show_selected_character_info(call, {'@': 'character_select', 'id': num, 'action': 'read'})
    await state.finish()


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


async def edit_clas(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await FSMCharacter.edit_class.set()

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

    await call.message.answer("Теперь выбери свой новый класс!", reply_markup=markup)


async def set_new_clas(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    async with state.proxy() as data:
        print("class" + data["id"])
    clas = callback_data.get("info")
    char_id = data["id"]
    num = data["num"]
    update_class(char_id, get_class_info(clas)[0][1])
    # edit character class = get_class_info(clas)[0][1]
    await show_selected_character_info(call, {'@': 'character_select', 'id': num, 'action': 'read'})
    await state.finish()


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


async def edit_origin(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await FSMCharacter.edit_origin.set()

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

    await call.message.answer("Теперь выбери своё новое происхождение!", reply_markup=markup)


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


async def set_new_origin(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    async with state.proxy() as data:
        print("origin" + data["id"])
    origin = callback_data.get("info")
    char_id = data["id"]
    num = data["num"]
    update_origin(char_id, get_origin_info(origin)[0][1])
    # edit character origin = get_origin_info(origin)[0][1]
    await show_selected_character_info(call, {'@': 'character_select', 'id': num, 'action': 'read'})
    await state.finish()


async def edit_level(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Введи свой новый уровень")
    await FSMCharacter.edit_level.set()


async def set_new_level(message: types.Message, state=FSMContext):
    try:
        level = int(message.text)
        async with state.proxy() as data:
            print("level" + data["id"])
        update_level(data["id"], level)
        # set character level = str(level)
        await message.answer("Новый уровень - " + message.text + ", установлен!", reply_markup=main_menu)
        await state.finish()

    except:
        await message.answer("Вот это да! Не знаю, как у вас, но у нас мастерство показывается с помощью числа. "
                             "Попробуй дать оценку своего уровня в виде числа!")


async def stop_creating_character(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(
        "Видимо сейчас ты не готов поделиться своей историей... Не переживай, я всегда буду здесь, чтобы"
        " послушать о твоих приключениях!", reply_markup=main_menu)


def register_character_editing(dp: Dispatcher):
    dp.register_callback_query_handler(edit_character, character_settings_callback.filter(setting="edit"), state='*')
    dp.register_callback_query_handler(edit_name, character_edit_callback.filter(info="name"), state=FSMCharacter.edit)
    dp.register_callback_query_handler(edit_race, character_edit_callback.filter(info="race"), state=FSMCharacter.edit)
    dp.register_callback_query_handler(edit_clas, character_edit_callback.filter(info="clas"), state=FSMCharacter.edit)
    dp.register_callback_query_handler(edit_origin, character_edit_callback.filter(info="origin"), state=FSMCharacter.edit)
    dp.register_callback_query_handler(edit_level, character_edit_callback.filter(info="level"), state=FSMCharacter.edit)
    dp.register_callback_query_handler(stop_creating_character, confirmation_callback.filter(choice="cancel"),
                                       state=FSMCharacter.all_states)

    dp.register_message_handler(set_new_name, state=FSMCharacter.edit_name)
    dp.register_message_handler(set_new_level, state=FSMCharacter.edit_level)

    # перелистывание страниц
    dp.register_callback_query_handler(next_page_race, page_button_callback.filter(action="next"),
                                       state=FSMCharacter.edit_race)
    dp.register_callback_query_handler(prev_page_race, page_button_callback.filter(action="prev"),
                                       state=FSMCharacter.edit_race)
    dp.register_callback_query_handler(next_page_class, page_button_callback.filter(action="next"),
                                       state=FSMCharacter.edit_class)
    dp.register_callback_query_handler(prev_page_class, page_button_callback.filter(action="prev"),
                                       state=FSMCharacter.edit_class)
    dp.register_callback_query_handler(next_page_origin, page_button_callback.filter(action="next"),
                                       state=FSMCharacter.edit_origin)
    dp.register_callback_query_handler(prev_page_origin, page_button_callback.filter(action="prev"),
                                       state=FSMCharacter.edit_origin)

    # подробная информация страниц
    dp.register_callback_query_handler(set_race_info, character_creation_callback.filter(type="race"),
                                       state=FSMCharacter.edit_race)
    dp.register_callback_query_handler(set_class_info, character_creation_callback.filter(type="class"),
                                       state=FSMCharacter.edit_class)
    dp.register_callback_query_handler(set_origin_info, character_creation_callback.filter(type="origin"),
                                       state=FSMCharacter.edit_origin)

    # повторный выбор
    dp.register_callback_query_handler(show_race_list, creation_confirmation_callback.filter(choice="no"),
                                       state=FSMCharacter.edit_race)
    dp.register_callback_query_handler(show_class_list, creation_confirmation_callback.filter(choice="no"),
                                       state=FSMCharacter.edit_class)
    dp.register_callback_query_handler(show_origin_list, creation_confirmation_callback.filter(choice="no"),
                                       state=FSMCharacter.edit_origin)

    # переход к следующему шагу
    dp.register_callback_query_handler(set_new_race, creation_confirmation_callback.filter(choice="yes"),
                                       state=FSMCharacter.edit_race)
    dp.register_callback_query_handler(set_new_clas, creation_confirmation_callback.filter(choice="yes"),
                                       state=FSMCharacter.edit_class)
    dp.register_callback_query_handler(set_new_origin, creation_confirmation_callback.filter(choice="yes"),
                                       state=FSMCharacter.edit_origin)

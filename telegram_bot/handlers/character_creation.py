from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from database.models.character_model import Character

from telegram_bot.keyboards.callback_datas import confirmation_callback, character_edit_callback, \
    character_creation_callback, page_button_callback
from telegram_bot.keyboards.inline import confirmation_menu, character_info, cancel_menu
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


races = ["Ааракокра 🪶", "Аасимар 👼", "Автогном ⚙️", "Астральный эльф 🔮", "Багбир 🐻", "Ведалкен 🧞", "Вердан 👺",
         "Гибрид Симиков 👽", "Гит 👹", "Гифф 🦛", "Гном 🧙‍", "Гоблин 🧌", "Голиаф 👁", "Грунг 🐸", "Дварф 🔨", "Дженази 🔥",
         "Драконорожденный 🐲", "Зайцегон 🐰", "Калаштар 👻", "Кендер 🦯", "Кенку 🦅", "Кентавр 🐎", "Кобольд 🐉",
         "Кованый ⛓", "Леонинец 🦁", "Локата 🐟", "Локсодон 🐘", "Людоящер 🦎", "Минотавр 🐂", "Орк 🐊",
         "Плазмоид 💦", "Полуорк 🧌", "Полурослик 👱", "Полуэльф 🧚", "Сатир 🐐", "Совлин 🦉", "Табакси 🐱",
         "Тифлинг 👿", "Тортл 🐢", "Три-крин 🦗", "Тритон 🐛", "Фейри 🧚", "Фриболг 🧞", "Хадози 🐵", "Хобгоблин 💀",
         "Чейнджоинг 🧟", "Человек 🤠", "Шифтер 🐶", "Эльф 🧝", "Юань-ти 🐍"]

classes = ["Бард 🪕", "Варвар 🪓", "Воин ⚔", "Волшебник 📖", "Друид 🌳", "Жрец ⚕", "Изобретатель ⚙",
           "Колдун 🧿", "Монах ⛪", "Паладин 🛡️", "Плут 🧤", "Следопыт 🔎", "Чародей 🔮"]

origins = ["Прислужник 📿", "Шарлатан 🃏", "Преступник 🦹", "Артист 🎤", "Народный герой 👮‍",
           "Гильдейский ремесленник 💰", "Отшельник 🌅", "Благородный 👑", "Чуземец 🌎",
           "Мудрец 🧔‍", "Моряк 🚢", "Солдат 🪖", "Беспризорник 👦"]

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

    button_list = []
    for i in range(0, 6, 2):
        button_list.append([InlineKeyboardButton(text=races[i], callback_data=character_creation_callback.new(
            action="race", race=races[i][:-2], clas="null", origin="null")), InlineKeyboardButton(text=races[i + 1],
                                                                                   callback_data=character_creation_callback.new(
                                                                                       action="race",
                                                                                       race=races[i + 1][:-2],
                                                                                       clas="null", origin="null"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page="1", action="prev")),
        InlineKeyboardButton(text="1", callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page="1", action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await message.reply(f'Что-то мне подсказывает, что происходит рождение нового героя - {data["name"]}, '
                        f'о ком барды будут складывать песни. А какие песни, решать уже тебе!')
    await message.answer('Выбери свою расу', reply_markup=markup)


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
            action="race", race=races[i][:-2], clas="null", origin="null")), InlineKeyboardButton(text=races[i + 1],
                                                                                   callback_data=character_creation_callback.new(
                                                                                       action="race",
                                                                                       race=races[i + 1][:-2],
                                                                                       clas="null",
                                                                                       origin="null"))])

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
            action="race", race=races[i][:-2], clas="null", origin="null")), InlineKeyboardButton(text=races[i + 1],
                                                                                   callback_data=character_creation_callback.new(
                                                                                       action="race",
                                                                                       race=races[i + 1][:-2],
                                                                                       clas="null",
                                                                                       origin="null"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev")),
        InlineKeyboardButton(text=str(data), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.edit_reply_markup(markup)


async def set_race(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()

    race = callback_data.get("race")
    async with state.proxy() as data:
        data['race'] = race
    await FSMCharacter.next()
    await call.message.edit_reply_markup(reply_markup=None)

    button_list = []
    for i in range(3):
        button_list.append([InlineKeyboardButton(text=classes[i], callback_data=character_creation_callback.new(
            action="clas", race="null", clas=classes[i][:-2], origin="null"))])

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

    if data > len(classes) / 3 + 1:
        return

    button_list = []
    for i in range((data - 1) * 3, data * 3):

        if i >= len(classes):
            break

        button_list.append([InlineKeyboardButton(text=classes[i], callback_data=character_creation_callback.new(
            action="clas", race="null", clas=classes[i][:-2], origin="null"))])

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
            action="clas", race="null", clas=classes[i][:-2], origin="null"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev")),
        InlineKeyboardButton(text=str(data), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.edit_reply_markup(markup)


async def set_clas(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    clas = callback_data.get("clas")
    async with state.proxy() as data:
        data['clas'] = clas
    await FSMCharacter.next()
    await call.message.edit_reply_markup(reply_markup=None)

    button_list = []
    for i in range(3):
        button_list.append([InlineKeyboardButton(text=origins[i], callback_data=character_creation_callback.new(
            action="origin", race="null", clas="null", origin=origins[i][:-2]))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page="1", action="prev")),
        InlineKeyboardButton(text="1", callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page="1", action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.answer(f'Хмм, {data["clas"]}... У него есть достойная история? Поведай ее или же выбери одно из предложенных сказаний', reply_markup=markup)

async def next_page_origin(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    data = int(callback_data.get("page")) + 1

    if data > len(origins) / 3 + 1:
        return

    button_list = []
    for i in range((data - 1) * 3, data * 3):

        if i >= len(origins):
            break

        button_list.append([InlineKeyboardButton(text=origins[i], callback_data=character_creation_callback.new(
            action="origin", race ="null", clas="null", origin=origins[i][:-2]))])

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
    for i in range((data - 1) * 3, data * 3):

        if i >= len(origins):
            break

        button_list.append([InlineKeyboardButton(text=origins[i], callback_data=character_creation_callback.new(
            action="race", race="null", clas="null", origin=origins[i][:-2]))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev")),
        InlineKeyboardButton(text=str(data), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next")),
        InlineKeyboardButton("Отменить создание", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.edit_reply_markup(markup)
async def set_origin(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    origin = callback_data.get("origin")
    async with state.proxy() as data:
        data['origin'] = origin
    await FSMCharacter.next()
    await call.message.reply(f'История от {data["origin"]} я еще не слыхал. Теперь скажи, какого уровня ты смог достичь?',
                        reply_markup=cancel_menu)

async def set_level(message: types.Message, state=FSMContext):
    try:
        async with state.proxy() as data:
            data['level'] = int(message.text)
        await FSMCharacter.next()
        await message.answer(f'Дай-ка запишу о тебе в своем блокноте\n\n-------------------\n'
                             f'🔅 Персонаж: {data["name"]} (уровень: {data["level"]})\n'
                             f'🧑‍🦳 Раса: {data["race"]}\n🧙 Класс: {data["clas"]}\n👼 Происхождение: {data["origin"]}\n-------------------\n'
                             f'\nПроверь меня, я все правильно услышал?', reply_markup=confirmation_menu)
    except:
        await message.answer("Вот это да! Не знаю, как у вас, но у нас мастерство показывается с помощью числа. "
                             "Попробуй дать оценку своего уровня в виде числа!")


async def save_character(call: types.CallbackQuery, state=FSMContext):
    await call.answer(cache_time=60)
    async with state.proxy() as data:
        Character.create(user_id = data["user_id"], name = data["name"], race = data["race"], clas = data["clas"],
                         origin = data["origin"], level = data["level"])
    await state.finish()
    await call.message.answer("Твоя история невероятна! Спасибо, что поделился ею со мной!")
    await call.message.edit_reply_markup(reply_markup=None)


async def stop_creating_character(call: types.CallbackQuery, state=FSMContext):
    await state.finish()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(
        "Видимо сейчас ты не готов поделиться своей историей... Не переживай, я всегда буду здесь, чтобы"
        " послушать о твоих приключениях!", reply_markup=main_menu)


def register_character_creation(dp: Dispatcher):
    dp.register_message_handler(create_character, Text(equals='Создать персонажа', ignore_case=True), state=None)
    dp.register_message_handler(stop_creating_character, Text(equals='Отменить создание персонажа', ignore_case=True),
                                state=FSMCharacter.all_states)
    dp.register_message_handler(set_name, state=FSMCharacter.name)
    # dp.register_message_handler(set_race, state=FSMCharacter.race)
    # dp.register_message_handler(set_clas, state=FSMCharacter.clas)
    dp.register_message_handler(set_origin, state=FSMCharacter.origin)
    dp.register_message_handler(set_level, state=FSMCharacter.level)

    dp.register_callback_query_handler(save_character, confirmation_callback.filter(choice="yes"),
                                       state=FSMCharacter.confirmation)
    dp.register_callback_query_handler(stop_creating_character, confirmation_callback.filter(choice="cancel"),
                                       state=FSMCharacter.all_states)

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
    dp.register_callback_query_handler(set_race, character_creation_callback.filter(action="race"),
                                       state=FSMCharacter.race)
    dp.register_callback_query_handler(set_clas, character_creation_callback.filter(action="clas"),
                                       state=FSMCharacter.clas)
    dp.register_callback_query_handler(set_origin, character_creation_callback.filter(action="origin"),
                                       state=FSMCharacter.origin)

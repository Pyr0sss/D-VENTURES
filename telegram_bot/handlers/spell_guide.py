import hashlib

from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import storage, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.db_processing.spell_processing import get_spell_info, search_spell_by_name
from telegram_bot.config import load_config
from telegram_bot.keyboards.callback_datas import page_button_callback, spell_read_callback, confirmation_callback
from telegram_bot.keyboards.reply import main_menu
from telegram_bot.misc import constants


class FSM(StatesGroup):
    search_text = State()
    show_text = State()


async def spell_guide_start(message: types.Message):
    button_list = []
    for i in range(1, 7):
        button_list.append([InlineKeyboardButton(text=str(get_spell_info(i)[0][1]),
                                                 callback_data=spell_read_callback.new(id=i, action="read"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page="1", action="prev")),
        InlineKeyboardButton(text="1", callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page="1", action="next")),
        InlineKeyboardButton("Магический поиск", callback_data=confirmation_callback.new(choice="search")),
        InlineKeyboardButton("Выйти из справочника", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await message.answer('Какое заклинание тебя заинтересовало?', reply_markup=markup)


async def next_spell(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    data = int(callback_data.get("page")) + 1

    if data >= constants.spells_counter / 6 + 1:
        return

    button_list = []
    for i in range((data - 1) * 6 + 1, data * 6 + 1):

        if i > constants.spells_counter:
            break

        button_list.append([InlineKeyboardButton(text=str(get_spell_info(i)[0][1]),
                                                 callback_data=spell_read_callback.new(id=i, action="read"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev")),
        InlineKeyboardButton(text=str(data), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next")),
        InlineKeyboardButton("Магический поиск", callback_data=confirmation_callback.new(choice="search")),
        InlineKeyboardButton("Выйти из справочника", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.edit_reply_markup(markup)


async def prev_spell(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    data = int(callback_data.get("page")) - 1

    if data < 1:
        return

    button_list = []
    for i in range((data - 1) * 6 + 1, data * 6 + 1):

        if i > constants.spells_counter:
            break

        button_list.append([InlineKeyboardButton(text=str(get_spell_info(i)[0][1]),
                                                 callback_data=spell_read_callback.new(id=i, action="read"))])

    markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=button_list)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev")),
        InlineKeyboardButton(text=str(data), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next")),
        InlineKeyboardButton("Магический поиск", callback_data=confirmation_callback.new(choice="search")),
        InlineKeyboardButton("Выйти из справочника", callback_data=confirmation_callback.new(choice="cancel"))
    )

    await call.message.edit_reply_markup(markup)


async def read_spell(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    spell = get_spell_info(callback_data.get("id"))
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Вернуться к справочнику",
                             callback_data=spell_read_callback.new(action="back", id=callback_data.get("id"))),
    )
    await call.message.answer(
        f"`{spell[0][1].upper()}`\n{spell[0][2]}-й уровень заклинания {get_class_availability(spell[0])}\n\n{spell[0][16]}", reply_markup=markup, parse_mode="Markdown")


async def return_to_spell_guide(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    await spell_guide_start(call.message)


async def start_search_spell(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    await FSM.search_text.set()
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="❎ Отменить поиск", callback_data=confirmation_callback.new(choice="stop")),
    )
    await call.message.edit_text(
        f"🔎 Поиск в справочнике\nЧтобы найти заклинания в книге, введи название, например, `Инферно`:",
        reply_markup=markup, parse_mode="Markdown")


async def spell_search(message: types.Message, state=FSMContext):
    text = message.text
    s = text[0].upper()
    for letter in text[1:]:
        s = s + letter.lower()
    spells = search_spell_by_name(s)
    async with state.proxy() as data:
        data['spells'] = spells
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(1), action="prev")),
        InlineKeyboardButton(text=str(1), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(1), action="next")),
        InlineKeyboardButton("Поиск", callback_data=confirmation_callback.new(choice="search"))
    )
    if len(spells) > 0:
        await FSM.next()
        reply = f"`{data['spells'][0][1].upper()}`\n{data['spells'][0][2]}-й уровень заклинание {get_class_availability(data['spells'][0])}\n\n{data['spells'][0][16]}"
        await message.answer(reply, reply_markup=markup, parse_mode="Markdown")
    else:
        reply = "🤷 Что-то я не помню таких магический штучек-дрючек..."
        await message.answer(reply)


async def spell_search_next(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    cur_page = int(callback_data.get("page")) + 1
    async with state.proxy() as data:
        spells = data['spells']
    if cur_page > len(spells):
        return
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(cur_page), action="prev")),
        InlineKeyboardButton(text=str(cur_page), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(cur_page), action="next")),
        InlineKeyboardButton("Поиск", callback_data=confirmation_callback.new(choice="search"))
    )
    reply = f"`{data['spells'][cur_page - 1][1].upper()}`\n{data['spells'][cur_page - 1][2]}-й уровень заклинание {get_class_availability(data['spells'][cur_page - 1])}\n\n{data['spells'][cur_page - 1][16]}"
    await call.message.edit_text(reply, reply_markup=markup, parse_mode="Markdown")


async def spell_search_prev(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer()
    cur_page = int(callback_data.get("page")) - 1
    async with state.proxy() as data:
        spells = data['spells']
    if cur_page < 1:
        return
    markup = InlineKeyboardMarkup(row_width=3)
    markup.add(
        InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(cur_page), action="prev")),
        InlineKeyboardButton(text=str(cur_page), callback_data="null"),
        InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(cur_page), action="next")),
        InlineKeyboardButton("Поиск", callback_data=confirmation_callback.new(choice="search"))
    )
    reply = f"`{data['spells'][cur_page - 1][1].upper()}`\n{data['spells'][cur_page - 1][2]}-й уровень заклинание {get_class_availability(data['spells'][cur_page - 1])}\n\n{data['spells'][cur_page - 1][16]}"
    await call.message.edit_text(reply, reply_markup=markup, parse_mode="Markdown")


async def stop_spell_search(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    await state.finish()
    await call.message.edit_text("🪬 Магия поиска испарилась")


async def search_spell_again(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    await state.finish()
    await spell_search(call.message)


async def spell_guide_quit(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("Хорошо, я тогда пойду и уберу эту большую книгу", reply_markup=main_menu)


def get_class_availability(spell):
    text = ""
    if spell[3] == '1': text = text + "Чародея, "
    if spell[4] == '1': text = text + "Колдуна, "
    if spell[5] == '1': text = text + "Волшебника, "
    if spell[6] == '1': text = text + "Барда, "
    if spell[7] == '1': text = text + "Жреца, "
    if spell[8] == '1': text = text + "Друида, "
    if spell[9] == '1': text = text + "Паладина, "
    if spell[10] == '1': text = text + "Изобретателя, "
    if spell[11] == '1': text = text + "Следопыта, "
    return text[:-2]


def register_spell_guide(dp: Dispatcher):
    dp.register_callback_query_handler(spell_search_next, page_button_callback.filter(action="next"),
                                       state=FSM.show_text)
    dp.register_callback_query_handler(spell_search_prev, page_button_callback.filter(action="prev"),
                                       state=FSM.show_text)

    dp.register_message_handler(spell_guide_start, Text(equals='Справочник', ignore_case=True), state='*')
    dp.register_callback_query_handler(next_spell, page_button_callback.filter(action="next"), state='*')
    dp.register_callback_query_handler(prev_spell, page_button_callback.filter(action="prev"), state='*')

    dp.register_callback_query_handler(return_to_spell_guide, spell_read_callback.filter(action="back"), state='*')
    dp.register_callback_query_handler(read_spell, spell_read_callback.filter(action="read"), state='*')

    dp.register_message_handler(spell_search, state=FSM.search_text)

    dp.register_callback_query_handler(spell_guide_quit, confirmation_callback.filter(choice="cancel"), state='*')
    dp.register_callback_query_handler(start_search_spell, confirmation_callback.filter(choice="search"), state='*')
    dp.register_callback_query_handler(stop_spell_search, confirmation_callback.filter(choice="stop"),
                                       state=FSM.search_text)

    dp.register_callback_query_handler(search_spell_again, confirmation_callback.filter(choice="search"),
                                       state=FSM.show_text)

import sqlite3

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
import sqlite3 as sq

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.db_processing.character_processing import read_limited_characters_page, get_character_info
from database.db_processing.spell_processing import search_spell_for_character
from telegram_bot.keyboards.callback_datas import character_select_callback, page_button_callback, \
    character_settings_callback
from telegram_bot.keyboards.inline import get_settings_menu, cancel_menu
from telegram_bot.keyboards.reply import main_menu


# меню выбора уже созданного персонажа (предлагается три варианта с перелистыванием страниц)
async def show_character_menu(message: types.Message):
    records = read_limited_characters_page(message.from_user.id)
    characters_buttons = []
    for i in range(3):
        if i >= len(records):
            break
        text = f'{records[i][2]} ({records[i][3]} - {records[i][6]} уровня)'
        characters_buttons.append([InlineKeyboardButton(text=text, callback_data=character_select_callback.new(
            id=i, action="read"
        ))])
        markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=characters_buttons)
        markup.add(
            InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(1), action="prev_char")),
            InlineKeyboardButton(text=str(1), callback_data="null"),
            InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(1), action="next_char")),
        )
    await message.answer("Выбери своего персонажа:", reply_markup=markup)


# если у пользователя нет созданных персонажей выполнится этот хендлер
async def show_warning_message(message: types.Message):
    await message.answer("Хмм... Твоих историй я еще не слыхал. Попробуй воспользоваться `Созданием персонажа`,"
                         " а потом возвращайся ко мне!", parse_mode='Markdown')


# Обработка нажатия на кнопку ">" - следующей страницы в просмотре созданных персонажей
async def show_next_character_page(call: types.CallbackQuery, callback_data: dict):
    global markup
    await call.answer()
    records = read_limited_characters_page(call.from_user.id)
    data = int(callback_data.get("page")) + 1
    if data > len(records) / 3 + 1:
        data = 1
    characters_buttons = []
    for i in range((data - 1) * 3, data * 3):
        if i >= len(records):
            break
        text = f'{records[i][2]} ({records[i][3]} - {records[i][6]} уровня)'
        characters_buttons.append([InlineKeyboardButton(text=text, callback_data=character_select_callback.new(
            id=i, action="read"
        ))])
        markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=characters_buttons)
        markup.add(
            InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev_char")),
            InlineKeyboardButton(text=str(data), callback_data="null"),
            InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next_char")),
        )
    await call.message.edit_reply_markup(reply_markup=markup)


# Обработка нажатия на кнопку "<" - предыдущей страницы в просмотре созданных персонажей
async def show_prev_character_page(call: types.CallbackQuery, callback_data: dict):
    global markup
    await call.answer()
    records = read_limited_characters_page(call.from_user.id)
    data = int(callback_data.get("page")) - 1
    if data < 1:
        data = int(len(records) / 3 + 1)
    characters_buttons = []
    for i in range((data - 1) * 3, data * 3):
        if i >= len(records):
            break
        text = f'{records[i][2]} ({records[i][3]} - {records[i][6]} уровня)'
        characters_buttons.append([InlineKeyboardButton(text=text, callback_data=character_select_callback.new(
            id=i, action="read"
        ))])
        markup = InlineKeyboardMarkup(row_width=3, inline_keyboard=characters_buttons)
        markup.add(
            InlineKeyboardButton(text="<", callback_data=page_button_callback.new(page=str(data), action="prev_char")),
            InlineKeyboardButton(text=str(data), callback_data="null"),
            InlineKeyboardButton(text=">", callback_data=page_button_callback.new(page=str(data), action="next_char")),
        )
    await call.message.edit_reply_markup(reply_markup=markup)


async def show_selected_character_info(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    records = read_limited_characters_page(call.from_user.id)
    i = int(callback_data.get("id"))
    text = f'🔅 Персонаж: {records[i][2]} (уровень: {records[i][6]})\n 🧑‍🦳 Раса: {records[i][3]}\n' \
           f'🧙 Класс: {records[i][4]}\n👼 Происхождение: {records[i][5]}'
    await call.message.edit_text(text, reply_markup=get_settings_menu(records[i][0], i))


async def show_available_spells(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    record = get_character_info(callback_data.get("id"))
    spells = search_spell_for_character(record[0][4], record[0][6])
    for spell in spells:
        await call.message.answer(f"`{spell[1]}` (уровень заклинания: {spell[2]})\n{spell[16]}", parse_mode="Markdown")


def register_character_selection(dp: Dispatcher):
    dp.register_message_handler(show_character_menu, Text(equals='Выбрать персонажа', ignore_case=True), state='*',
                                has_character=True)
    dp.register_message_handler(show_warning_message, Text(equals='Выбрать персонажа', ignore_case=True), state='*',
                                has_character=False)
    dp.register_callback_query_handler(show_next_character_page, page_button_callback.filter(action="next_char"))
    dp.register_callback_query_handler(show_prev_character_page, page_button_callback.filter(action="prev_char"))
    dp.register_callback_query_handler(show_selected_character_info, character_select_callback.filter(action="read"))
    dp.register_callback_query_handler(show_available_spells, character_settings_callback.filter(setting="spells"))

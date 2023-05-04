import sqlite3

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
import sqlite3 as sq

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from telegram_bot.keyboards.callback_datas import character_select_callback, page_button_callback


# меню выбора уже созданного персонажа (предлагается три варианта с перелистыванием страниц)
# TODO: выбор "Выбрать персонажа" должен также отменять создание персонажа, как это делает кнопка "Отменить создание"
async def show_character_menu(message: types.Message):
    global markup
    records = read_limited_characters_page(message.from_user.id)
    characters_buttons = []
    for i in range(3):
        if i >= len(records):
            break
        text = f'{records[i][1]} ({records[i][3]} - {records[i][5]} уровня)'
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


# Обработка нажатия на кнопку ">" - следующей страницы в просмотре созданных персонажей
# TODO: необходимо оптимизировать запрос с перелистыванием (например, три раза вперед, один назад)
# TODO: решить ошибку "Message is not modified: specified new message content and reply markup are exactly the same as
#  a current content and reply markup of the message"
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
        text = f'{records[i][1]} ({records[i][3]} - {records[i][5]} уровня)'
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
        text = f'{records[i][1]} ({records[i][3]} - {records[i][5]} уровня)'
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
    await call.message.edit_reply_markup(reply_markup=None)
    records = read_limited_characters_page(call.from_user.id)
    i = int(callback_data.get("id"))
    text = f'🔅 Персонаж: {records[i][1]} (уровень: {records[i][5]})\n 🧑‍🦳 Раса: {records[i][2]}\n' \
           f'🧙 Класс: {records[i][3]}\n👼 Происхождение: {records[i][4]}'
    await call.message.edit_text(text)


# получение определенного количества строк из БД посредством проверки по user_id
def read_limited_characters_page(user_id):
    global base
    try:
        base = sq.connect('dnd.db')
        cursor = base.cursor()
        query = "SELECT * FROM Characters WHERE user_id = " + str(user_id)
        cursor.execute(query)
        record = cursor.fetchall()
        cursor.close()
        return record

    except sqlite3.Error as error:
        print("Ошибка в работе с SQLite ", error)
    finally:
        if base:
            base.close()


def register_character_selection(dp: Dispatcher):
    dp.register_message_handler(show_character_menu, Text(equals='Выбрать персонажа', ignore_case=True), state='*')
    dp.register_callback_query_handler(show_next_character_page, page_button_callback.filter(action="next_char"))
    dp.register_callback_query_handler(show_prev_character_page, page_button_callback.filter(action="prev_char"))
    dp.register_callback_query_handler(show_selected_character_info, character_select_callback.filter(action="read"))

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.db_processing.character_processing import read_limited_characters_page
from database.db_processing.qualities_processing import get_total_qualities, get_qualities_info
from database.models.qualities_model import Quality
from telegram_bot.keyboards.callback_datas import character_settings_callback
from telegram_bot.keyboards.inline import get_settings_menu
from telegram_bot.misc.dice_throwing import throw_dice_20


async def calculate_qualities(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    if get_total_qualities(callback_data.get("id")) > 0:
        record = get_qualities_info(callback_data.get("id"))
        print(callback_data.get("id"))
        text = f'Сила: {record[0][3]}\nЛовкость: {record[0][4]}\nТелосложение: {record[0][5]}\nИнтеллект: {record[0][6]}\nМудрость: {record[0][7]}\nХаризма: {record[0][8]}\n'
        await call.message.answer(text, reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=[[
            InlineKeyboardButton(text="◀️ Назад", callback_data=character_settings_callback.new(setting="back",
                                                                                                id=callback_data.get(
                                                                                                    "id"),
                                                                                                num=callback_data.get(
                                                                                                    "num")))]]))
        return

    await call.message.answer("Доверимся проведению!")
    async with state.proxy() as data:
        data["force"] = await throw_dice_20(call.message)
    await call.message.answer("Запишем это значение в ваш уровень силы. Продолжаем!")
    async with state.proxy() as data:
        data["agility"] = await throw_dice_20(call.message)
    await call.message.answer("А это теперь ваша ловкость! Перейдем к телосложению.")
    async with state.proxy() as data:
        data["body"] = await throw_dice_20(call.message)
    await call.message.answer("Феноменально! А что насчет интеллекта?")
    async with state.proxy() as data:
        data["intellect"] = await throw_dice_20(call.message)
    await call.message.answer("Отличный результат! Переходим к мудрости.")
    async with state.proxy() as data:
        data["wisdom"] = await throw_dice_20(call.message)
    await call.message.answer("Осталась только харизма!")
    async with state.proxy() as data:
        data["charisma"] = await throw_dice_20(call.message)
    async with state.proxy() as data:
        Quality.create(user_id=call.message.from_user.id, character_id=callback_data.get("id"), force=data["force"],
                       agility=data["agility"],
                       body=data["body"], intellect=data["intellect"], wisdom=data['wisdom'], charisma=data["charisma"])
    record = get_qualities_info(callback_data.get("id"))
    print(callback_data.get("id"))
    text = f'Сила: {record[0][3]}\nЛовкость: {record[0][4]}\nТелосложение: {record[0][5]}\nИнтеллект: {record[0][6]}\nМудрость: {record[0][7]}\nХаризма: {record[0][8]}\n'
    await call.message.answer(text, reply_markup=InlineKeyboardMarkup(row_width=1, inline_keyboard=[[
        InlineKeyboardButton(text="◀️ Назад",
                             callback_data=character_settings_callback.new(setting="back", id=callback_data.get("id"),
                                                                           num=callback_data.get("num")))]]))


async def page_return(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=None)
    records = read_limited_characters_page(call.from_user.id)
    i = int(callback_data.get("num"))
    text = f'🔅 Персонаж: {records[i][2]} (уровень: {records[i][6]})\n 🧑‍🦳 Раса: {records[i][3]}\n' \
           f'🧙 Класс: {records[i][4]}\n👼 Происхождение: {records[i][5]}'
    await call.message.answer(text, reply_markup=get_settings_menu(records[i][0], i))


def register_qualities(dp: Dispatcher):
    dp.register_callback_query_handler(calculate_qualities, character_settings_callback.filter(setting="qualities"),
                                       state='*')
    dp.register_callback_query_handler(page_return, character_settings_callback.filter(setting="back"),
                                       state='*')

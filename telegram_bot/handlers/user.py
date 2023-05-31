from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from telegram_bot.keyboards.reply import ready, main_menu
from telegram_bot.misc.throttling import rate_limit

from database.models.user_model import User
from database.db_processing.user_processing import user_existence_check
from database.db_processing.db_creation import db_creation
from telegram_bot.misc.dice_throwing import throw_dice


@rate_limit(1)
async def user_welcome(message: types.Message):
    text = "Здравствуй, дорогой путешественник! Добро пожаловать в D&VENTURES! " \
           "Готов ли ты полностью погрузиться в захватывающее приключение? " \
           "Если так, то этот бот поможет сделать его еще более увлекательным и незабываемым!\nГотов к бою?"
    if not user_existence_check(message.from_user.id):
        print("meow")
        User.create(user_id=message.from_user.id, username=message.from_user.first_name, is_banned=0)
    return await message.answer(text, reply_markup=ready)


@rate_limit(3, key='start')
async def user_main_menu(message: types.Message):
    text = "Здравствуй, таинственный незнакомец! Присядь, выпей бренди на дорожку и поведай мне кто ты таков? " \
           "Ежели твоя волшебная идентичность еще не определена, то советую заглянуть в древний магический справочник" \
           " – он поможет с выбором и поведает тебе обо всем на свете."
    return await message.answer(text, reply_markup=main_menu)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_welcome, commands=['start'], state='*')
    dp.register_message_handler(user_main_menu, Text(equals='В бой!', ignore_case=True), state='*')

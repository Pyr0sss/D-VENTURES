from _ast import Lambda

from aiogram import types, Dispatcher

from telegram_bot.keyboards.reply import ready, main_menu


async def user_welcome(message: types.Message):
    text = "Здравствуй, дорогой путешественник! Добро пожаловать в D&VENTURES! " \
           "Готов ли ты полностью погрузиться в захватывающее приключение? " \
           "Если так, то этот бот поможет сделать его еще более увлекательным и незабываемым! Готов к бою?"
    await message.answer(text, reply_markup=ready)


async def user_main_menu(message: types.Message):
    if message.text == "В бой!":
        text = "Здравствуй, таинственный незнакомец! Присядь, выпей бренди на дорожку и поведай мне кто ты таков? " \
               "Ежели твоя волшебная идентичность еще не определена, то советую заглянуть в древний магический справочник" \
               " – он поможет с выбором и поведает тебе обо всем на свете."
        await message.answer(text, reply_markup=main_menu)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_welcome, commands=['start'])
    dp.register_message_handler(user_main_menu)

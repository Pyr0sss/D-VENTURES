from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode


async def user_welcome(message: types.Message):
    text = "Здравствуй, дорогой путешественник! Добро пожаловать в D&VENTURES! " \
           "Готов ли ты полностью погрузиться в захватывающее приключение? " \
           "Если так, то этот бот поможет сделать его еще более увлекательным и незабываемым. В бой!"
    await message.answer(text)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_welcome, commands=['start'])


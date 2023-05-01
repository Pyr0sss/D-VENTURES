from mock import AsyncMock

import pytest

from telegram_bot.handlers.user import user_welcome, user_main_menu
from telegram_bot.keyboards.reply import ready, main_menu


@pytest.mark.asyncio
async def test_start_handler():
    message = AsyncMock()
    await user_welcome(message)
    text = "Здравствуй, дорогой путешественник! Добро пожаловать в D&VENTURES! " \
           "Готов ли ты полностью погрузиться в захватывающее приключение? " \
           "Если так, то этот бот поможет сделать его еще более увлекательным и незабываемым!\nГотов к бою?"
    message.answer.assert_called_with(text, reply_markup=ready)


@pytest.mark.asyncio
async def test_start_bot_handler():
    message = AsyncMock()
    await user_main_menu(message)
    text = "Здравствуй, таинственный незнакомец! Присядь, выпей бренди на дорожку и поведай мне кто ты таков? " \
           "Ежели твоя волшебная идентичность еще не определена, то советую заглянуть в древний магический справочник" \
           " – он поможет с выбором и поведает тебе обо всем на свете."
    message.answer.assert_called_with(text, reply_markup=main_menu)

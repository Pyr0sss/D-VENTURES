from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot.keyboards.callback_datas import confirmation_callback

confirmation_menu = InlineKeyboardMarkup(row_width=2,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(
                                                     text="Нет",
                                                     callback_data=confirmation_callback.new(choice="no")
                                                 ),
                                                 InlineKeyboardButton(
                                                     text="Да",
                                                     callback_data=confirmation_callback.new(choice="yes")
                                                 )
                                             ]
                                         ])

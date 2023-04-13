from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
ready = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='В бой!')
        ],
    ],
    resize_keyboard=True
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Справочник')
        ],
    ],
    resize_keyboard=True
)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
ready = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='В бой! 🏹')
        ],
    ],
    resize_keyboard=True
)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Справочник 📮'),  KeyboardButton(text='Создать персонажа 🖍️'),
            KeyboardButton(text='Помощь ❓')
        ],
    ],
    resize_keyboard=True
)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Просмотр статистики'),
            KeyboardButton(text='Заблокированные пользователи'),
        ],
        [
            KeyboardButton(text='Добавить заклинание'),
            KeyboardButton(text='Удалить заклинание'),
        ],
        [
            KeyboardButton(text='Вернуться к основному функционалу'),
        ],
    ],
    resize_keyboard=True
)

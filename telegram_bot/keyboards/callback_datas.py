from aiogram.utils.callback_data import CallbackData

confirmation_callback = CallbackData("confirmation", "choice")
character_edit_callback = CallbackData("character_edit", "info")
character_race_callback = CallbackData("character_race", "action", "race")
page_button_callback = CallbackData("page_button", "page", "action")

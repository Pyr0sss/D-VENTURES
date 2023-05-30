from aiogram.utils.callback_data import CallbackData

confirmation_callback = CallbackData("confirmation", "choice")
character_edit_callback = CallbackData("character_edit", "info")
character_creation_callback = CallbackData("character_creation", "action", "race", "clas")
page_button_callback = CallbackData("page_button", "page", "action")
character_select_callback = CallbackData("character_select", "id", "action")

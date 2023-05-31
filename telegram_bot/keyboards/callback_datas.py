from aiogram.utils.callback_data import CallbackData

confirmation_callback = CallbackData("confirmation", "choice")
character_edit_callback = CallbackData("character_edit", "info")
character_creation_callback = CallbackData("character_creation", "info", "type")
creation_confirmation_callback = CallbackData("creation_confirmation", "choice", "info")
character_settings_callback = CallbackData("character_settings", "setting", "id", "num")
page_button_callback = CallbackData("page_button", "page", "action")
character_select_callback = CallbackData("character_select", "id", "action")

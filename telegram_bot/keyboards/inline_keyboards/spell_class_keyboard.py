from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot.keyboards.callback_datas import spell_class_callback, confirmation_callback

spell_class = InlineKeyboardMarkup(row_width=1,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(text="Бард",callback_data=spell_class_callback.new(turn="off", name="Барда, ", clas="class_bard"))
                                       ],
                                       [
                                           InlineKeyboardButton(text="Волшебник", callback_data=spell_class_callback.new(turn="off", name="Волшебника, ", clas="class_sorcerer"))
                                       ],
                                       [
                                           InlineKeyboardButton(text="Друид",callback_data=spell_class_callback.new(turn="off", name="Друида, ", clas="class_druid"))
                                       ],
                                       [
                                           InlineKeyboardButton( text="Жрец",callback_data=spell_class_callback.new(turn="off", name="Жреца, ", clas="class_cleric"))
                                       ],
                                       [
                                           InlineKeyboardButton(text="Изобретатель",callback_data=spell_class_callback.new(turn="off", name="Изобретателя, ", clas="class_artificer"))
                                       ],
                                       [
                                           InlineKeyboardButton(text="Колдун",callback_data=spell_class_callback.new(turn="off", name="Колдуна, ", clas="class_warlock"))
                                       ],
                                       [
                                           InlineKeyboardButton(text="Паладин",callback_data=spell_class_callback.new(turn="off", name="Паладина, ", clas="class_paladin"))
                                       ],
                                       [
                                           InlineKeyboardButton(text="Следопыт",callback_data=spell_class_callback.new(turn="off", name="Следопыта, ", clas="class_ranger"))
                                       ],
                                       [
                                           InlineKeyboardButton(text="Чародей",callback_data=spell_class_callback.new(turn="off", name="Чародея, ", clas="class_wizard"))
                                       ],
                                       [
                                           InlineKeyboardButton(text="Завершить выбор классов ✅", callback_data=confirmation_callback.new(choice="yes"))
                                       ],
                                   ])

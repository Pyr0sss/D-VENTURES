from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot.keyboards.callback_datas import confirmation_callback, character_edit_callback, \
    character_settings_callback

cancel_menu = InlineKeyboardMarkup(row_width=1,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(
                                               text="Отменить создание",
                                               callback_data=confirmation_callback.new(choice="cancel")
                                           )
                                       ]
                                   ])

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
                                             ],
                                             [
                                                 InlineKeyboardButton(
                                                     text="Отменить создание",
                                                     callback_data=confirmation_callback.new(choice="cancel")
                                                 )
                                             ]
                                         ])

character_info = InlineKeyboardMarkup(row_width=1,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(
                                                  text="Имя персонажа",
                                                  callback_data=character_edit_callback.new(info="name")
                                              )
                                          ],
                                          [
                                              InlineKeyboardButton(
                                                  text="Расу персонажа",
                                                  callback_data=character_edit_callback.new(info="race")
                                              ),
                                          ],
                                          [
                                              InlineKeyboardButton(
                                                  text="Класс персонажа",
                                                  callback_data=character_edit_callback.new(info="clas")
                                              ),
                                          ],
                                          [
                                              InlineKeyboardButton(
                                                  text="Происхождение персонажа",
                                                  callback_data=character_edit_callback.new(info="origin")
                                              ),
                                          ],
                                          [
                                              InlineKeyboardButton(
                                                  text="Уровень персонажа",
                                                  callback_data=character_edit_callback.new(info="level")
                                              )
                                          ],
                                      ]
                                      )


def get_settings_menu(char_id, i):
    return InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(
                                            text="Изменить данные",
                                            callback_data=character_settings_callback.new(setting="edit", id=char_id, num=i)
                                        ),

                                        InlineKeyboardButton(
                                            text="Удалить персонажа",
                                            callback_data=character_settings_callback.new(setting="delete", id=char_id, num=i)
                                        ),
                                    ],
                                    [
                                        InlineKeyboardButton(
                                            text="Просмотреть доступные заклинания",
                                            callback_data=character_settings_callback.new(setting="spells", id=char_id,
                                                                                          num=i)
                                        )
                                    ]
                                ]
                                )

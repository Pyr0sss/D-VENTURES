from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot.keyboards.callback_datas import character_race_callback

character_race_1 = InlineKeyboardMarkup(row_width=3,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(
                                                    text="Ааракокра 🪶",
                                                    callback_data=character_race_callback.new(race="Ааракокра")
                                                ),

                                                InlineKeyboardButton(
                                                    text="Аасимар 👼",
                                                    callback_data=character_race_callback.new(race="Аасимар")
                                                )
                                            ],
                                            [
                                                InlineKeyboardButton(
                                                    text="Автогном ⚙️",
                                                    callback_data=character_race_callback.new(race="Автогном")
                                                ),

                                                InlineKeyboardButton(
                                                    text="Астральный эльф 🔮",
                                                    callback_data=character_race_callback.new(race="Астральный эльф")
                                                )
                                            ],
                                            [
                                                InlineKeyboardButton(
                                                    text="Багбир 🐻",
                                                    callback_data=character_race_callback.new(race="Багбир")
                                                ),

                                                InlineKeyboardButton(
                                                    text="Ведалкен 🧞",
                                                    callback_data=character_race_callback.new(race="Ведалкен")
                                                )
                                            ]
                                        ])

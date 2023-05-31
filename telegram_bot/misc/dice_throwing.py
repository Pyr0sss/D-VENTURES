from aiogram import Bot, types, Dispatcher
import time
import random
from telegram_bot.config import load_config

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
sticker="CAACAgIAAxkBAAEJLC5kd6rpkBKkbnqqYreFX_SpkI6xAQAC324AAp7OCwABhEHLNbbuyegvBA"

async def throw_dice(message: types.Message):
    await bot.send_sticker(message.chat.id, sticker)
    rez = random.randint(1, 20)
    time.sleep(3)
    await message.answer('Вам выпало '+ str(rez) + '!')

def register_dice(dp: Dispatcher):
    dp.register_message_handler(throw_dice, commands=['throw'], state='*')
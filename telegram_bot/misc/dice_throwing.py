from aiogram import Bot, types, Dispatcher
import time
import random
from telegram_bot.config import load_config

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
sticker="CAACAgIAAxkBAAEJLC5kd6rpkBKkbnqqYreFX_SpkI6xAQAC324AAp7OCwABhEHLNbbuyegvBA"

async def throw_dice_20(message: types.Message):
    await bot.send_sticker(message.chat.id, sticker)
    rez = random.randint(1, 20)
    time.sleep(3)
    await message.answer('Вам выпало '+ str(rez) + '!')
    return rez

async def throw_dice_4(message: types.Message):
    await bot.send_sticker(message.chat.id, sticker)
    rez = random.randint(1, 4)
    time.sleep(3)
    await message.answer('Вам выпало '+ str(rez) + '!')

async def throw_dice_8(message: types.Message):
    await bot.send_sticker(message.chat.id, sticker)
    rez = random.randint(1, 8)
    time.sleep(3)
    await message.answer('Вам выпало '+ str(rez) + '!')

async def throw_dice_6(message: types.Message):
    await bot.send_sticker(message.chat.id, sticker)
    rez = random.randint(1, 6)
    time.sleep(3)
    await message.answer('Вам выпало '+ str(rez) + '!')

async def throw_dice_10(message: types.Message):
    await bot.send_sticker(message.chat.id, sticker)
    rez = random.randint(1, 10)
    time.sleep(3)
    await message.answer('Вам выпало '+ str(rez) + '!')

async def throw_dice_100(message: types.Message):
    await bot.send_sticker(message.chat.id, sticker)
    rez = random.randint(1, 100)
    time.sleep(3)
    await message.answer('Вам выпало '+ str(rez) + '!')

def register_dice(dp: Dispatcher):
    dp.register_message_handler(throw_dice_4, commands=['throw4'], state='*')
    dp.register_message_handler(throw_dice_6, commands=['throw6'], state='*')
    dp.register_message_handler(throw_dice_8, commands=['throw8'], state='*')
    dp.register_message_handler(throw_dice_10, commands=['throw10'], state='*')
    dp.register_message_handler(throw_dice_20, commands=['throw20'], state='*')
    dp.register_message_handler(throw_dice_100, commands=['throw100'], state='*')
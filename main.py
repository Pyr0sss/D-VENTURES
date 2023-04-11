from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

bot = Bot(token="6197057580:AAH9Dj6kRrCKASuy7FRfB2eFZP-XJJTp0Q8")
dp = Dispatcher(bot)


@dp.message_handler()
async def get_message(message: types.Message):
    chat_id = message.chat.id
    username = "Привет @" + message.from_user.username
    text = username

    await bot.send_message(chat_id=chat_id, text=text)
    await bot.send_photo(chat_id=chat_id,
                         photo="https://i.pinimg.com/originals/f4/d2/96/f4d2961b652880be432fb9580891ed62.png")


executor.start_polling(dp)

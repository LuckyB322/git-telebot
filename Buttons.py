from aiogram import Bot, types
from config import bot_token
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import weather_token
import requests

bot = Bot(bot_token)
dp = Dispatcher(bot)


b=input('gorod')
r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={b}&appid={weather_token}&units=metric")
print(requests.codes.ok)





"""@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["С пюрешкой", "Без пюрешки"]
    keyboard.add(*buttons)
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!", reply_markup=types.ReplyKeyboardRemove())



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)"""

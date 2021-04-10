import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json
from config import bot_token, weather_token
from Weather import start_command

bot = Bot(bot_token)
dp = Dispatcher(bot)
URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'


@dp.message_handler(commands='kurs')
async def start_command_kurs(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["USD", "EUR", "RUR", "BTC"]
    keyboard.add(*buttons)
    await message.answer("Привет! Выбери валюту\U0001F4B8:", reply_markup=keyboard)

    @dp.message_handler()
    async def get_exchange(message: types.Message):
        data = (json.loads(requests.get(URL).text))
        for exc in data:
            if message.text == exc['ccy'] and message.text != 'BTC':
                await message.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                     f'\U0001F4B0{message.text}\nПродажа : {exc["buy"]}₴\n'
                                     f'Покупка : {exc["sale"]}₴\n ', reply_markup=types.ReplyKeyboardRemove())
            elif message.text == exc['ccy']:
                await message.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                     f'\U0001F4B0{message.text}\nПродажа : {exc["buy"]}$\n'
                                     f'Покупка : {exc["sale"]}$', reply_markup=types.ReplyKeyboardRemove())
                pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

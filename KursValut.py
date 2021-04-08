import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json
from config import bot_token

bot = Bot(bot_token)
dp = Dispatcher(bot)
URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'


@dp.message_handler(commands=['kurs'])
async def start_command(message: types.Message):
    await message.answer("Привет! Доступны валюты USD EUR RUR BTC")

    @dp.message_handler()
    async def get_exchange(message: types.Message):
        data = (json.loads(requests.get(URL).text))
        for exc in data:
            if message.text == exc['ccy'] and message.text != 'BTC':
                await message.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                     f'{message.text}\nПродажа : {exc["buy"]}грн \n'
                                     f'Покупка : {exc["sale"]}грн \n ')
            elif message.text == exc['ccy']:
                await message.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                     f'{message.text}\nПродажа : {exc["buy"]} usd \n'
                                     f'Покупка : {exc["sale"]} usd \n ')
                pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

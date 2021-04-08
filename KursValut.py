import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json

bot = Bot('1714723890:AAGFc4z3h3fTsy_k1jhesajH1QXjGuzqzV0')
dp = Dispatcher(bot)
URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'


@dp.message_handler(commands=['kurs'])
async def start_command(message: types.Message):
    await message.reply("Привет! Доступны валюты USD EUR BTC")

    @dp.message_handler()
    async def get_exchange(message: types.Message):
        data = (json.loads(requests.get(URL).text))
        for exc in data:
            if message.text == exc['ccy']:
                await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*** \n"
                                    f'{message.text}\nПокупка : {exc["buy"]}грн \n'
                                    f'Продажа : {exc["sale"]}грн \n ')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json
from config import bot_token


URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
print(requests.get(URL).text)
data = (json.loads(requests.get(URL).text))
print(data)

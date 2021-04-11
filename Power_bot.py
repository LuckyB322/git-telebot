import requests
import datetime
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import json
from config import weather_token, second_bot_token
from asyncio import sleep

bot = Bot(second_bot_token)
dp = Dispatcher(bot)
URL = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'


@dp.message_handler(commands=['start'])
async def start_command_bot(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Kurs", "Weather", "Bones"]
    keyboard.add(*buttons)
    await message.answer("Выбери действие\U0001F4B8:", reply_markup=keyboard)

    @dp.message_handler(text="Kurs")
    async def start_command_kurs(message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["USD", "EUR", "RUR", "BTC"]
        keyboard.add(*buttons)
        await message.answer("Выбери валюту\U0001F4B8:", reply_markup=keyboard)

        @dp.message_handler(text=["USD", "EUR", "RUR", "BTC"])
        async def get_exchange(message: types.Message):
            data = (json.loads(requests.get(URL).text))
            for exc in data:
                if message.text == exc['ccy'] and message.text != 'BTC':
                    await message.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                         f'\U0001F4B0UAH -> {message.text}:\nПродажа : {exc["buy"]}₴\n'
                                         f'Покупка : {exc["sale"]}₴\n ', reply_markup=types.ReplyKeyboardRemove())
                elif message.text == exc['ccy']:
                    await message.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                         f'\U0001F4B0 USD -> {message.text}:\nПродажа : {exc["buy"]}$\n'
                                         f'Покупка : {exc["sale"]}$', reply_markup=types.ReplyKeyboardRemove())
                    break
            return await start_command_bot(message)
    @dp.message_handler(text='Weather')
    async def start_command(message: types.Message):
        await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды!",
                            reply_markup=types.ReplyKeyboardRemove())

        @dp.message_handler()
        async def get_weather(message: types.Message):
            code_to_smile = {
                "Clear": "Ясно \U00002600",
                "Clouds": "Облачно \U00002601",
                "Rain": "Дождь \U00002614",
                "Drizzle": "Дождь \U00002614",
                "Thunderstorm": "Гроза \U000026A1",
                "Snow": "Снег \U0001F328",
                "Mist": "Туман \U0001F32B"
            }

            try:
                r = requests.get(
                    f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric"
                )

                data = r.json()

                city = data["name"]
                cur_weather = data["main"]["temp"]

                weather_description = data["weather"][0]["main"]
                if weather_description in code_to_smile:
                    wd = code_to_smile[weather_description]
                else:
                    wd = "Посмотри в окно, не пойму что там за погода!"

                humidity = data["main"]["humidity"]
                pressure = data["main"]["pressure"]
                wind = data["wind"]["speed"]
                sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
                sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
                length_of_the_day = datetime.datetime.fromtimestamp(
                    data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                    data["sys"]["sunrise"])

                await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                    f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                                    f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                    f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                    f"***Хорошего дня!***"
                                    )

            except KeyError:
                await message.reply("\U00002620 Проверьте название города \U00002620")
                return await get_weather(message)


    @dp.message_handler(text='Bones')
    async def on_message(message: types.Message):
        text = f'Привет, {message.from_user.full_name} \U0001F604!\nИгра проста: кидаю два кубика, первый - мне, второй - тебе,' \
               f'у кого больше - тот и победил. Поехали? \U00002666'

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Бросай!", "Не люблю игры."]
        keyboard.add(*buttons)
        await message.answer(text, reply_markup=keyboard)

        @dp.message_handler(text=("Бросай!", "Не люблю игры."))
        async def on_message(message: types.Message):
            if message.text == "Бросай!":
                bot_data = await bot.send_dice(message.chat.id, reply_markup=types.ReplyKeyboardRemove())
                bot_data = bot_data['dice']['value']
                await sleep(5)

                user_data = (await bot.send_dice(message.chat.id))
                user_data = (user_data['dice']['value'])
                await sleep(5)

                if bot_data > user_data:
                    await message.answer('Ты проиграл! \U0001F622')
                elif bot_data < user_data:
                    await message.answer('Ты выиграл! \U0000270B')
                else:
                    await message.answer('Ничья! \U0001F4A5')
            elif message.text == "Не люблю игры.":
                await message.answer("Хорошо, я буду тебя ждать здесь \U0001F436",
                                     reply_markup=types.ReplyKeyboardRemove())
            return await start_command_bot(message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

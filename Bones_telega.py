from aiogram import Bot, Dispatcher, types, executor
from asyncio import sleep
from config import bot_token

bot = Bot(bot_token)

dp = Dispatcher(bot)


@dp.message_handler(commands='bones')
async def on_message(message: types.Message):
    text = f'Привет, {message.from_user.username} \U0001F604!\nИгра проста: кидаю два кубика, первый - мне, второй - тебе,' \
           f'у кого больше - тот и победил. Поехали? \U00002666'

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Бросай!", "Не люблю игры."]
    keyboard.add(*buttons)
    await message.answer(text, reply_markup=keyboard)

    @dp.message_handler()
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
            await message.answer("Хорошо, я буду тебя ждать здесь \U0001F436", reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

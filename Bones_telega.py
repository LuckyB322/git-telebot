from aiogram import Bot, Dispatcher, types, executor
from asyncio import sleep
from config import bot_token

bot = Bot(bot_token)

dp = Dispatcher(bot)


@dp.message_handler()
async def on_message(message: types.Message):
    text = f'Привет, {message.from_user.username} !\nИгра проста: кидаю два кубика, первый - мне, второй - тебе,' \
           f'у кого больше - тот и победил. Поехали!'
    await message.answer(text)
    await sleep(5)

    bot_data = await bot.send_dice(message.chat.id)
    bot_data = bot_data['dice']['value']
    await sleep(5)

    user_data = (await bot.send_dice(message.chat.id))
    user_data = (user_data['dice']['value'])
    await sleep(5)

    if bot_data > user_data:
        await message.answer('Ты проиграл!')
    elif bot_data < user_data:
        await message.answer('Ты выиграл!')
    else:
        await message.answer('Ничья!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

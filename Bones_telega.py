from aiogram import Bot, Dispatcher, types, executor
from asyncio import sleep

# chat_id = -1001319214051
group_id = -539729788
bot = Bot('1714723890:AAGFc4z3h3fTsy_k1jhesajH1QXjGuzqzV0')

dp = Dispatcher(bot)

#comment

@dp.message_handler()
async def on_message(message: types.Message):
    text = f'Привет, {message.from_user.username} !\nИгра проста: кидаю два кубика, первый - мне, второй - тебе, у кого больше - тот и победил. Поехали!'
    await bot.send_message(message.chat.id, text=text)
    await sleep(5)

    bot_data = await bot.send_dice(message.chat.id)
    bot_data = bot_data['dice']['value']
    await sleep(5)

    user_data = (await bot.send_dice(message.chat.id))
    user_data = (user_data['dice']['value'])
    await sleep(5)

    if bot_data > user_data:
        await bot.send_message(message.chat.id, text='Ты проиграл!')
    elif bot_data < user_data:
        await bot.send_message(message.chat.id, text='Ты выиграл!')
    else:
        await bot.send_message(message.chat.id, text='Ничья!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

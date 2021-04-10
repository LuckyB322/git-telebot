import time
import asyncio


'''async def waiter() -> None:
    await cook('Паста', 1)
    await cook('Салат Цезарь', 2)
    await cook('Отбивные', 16)

def waiter():
    cook('Паста', 8)
    cook('Салат Цезарь', 3)
    cook('Отбивные', 16)

async def cook(order, time_to_prepare):
    print(f'Новый заказ: {order}')
    await asyncio.sleep(time_to_prepare)
    print(order, '- готово')


def cook(order, time_to_prepare):
    print(f'Новый заказ: {order}')
    time.sleep(time_to_prepare)
    print(order, '- готово')

if __name__ == '__main__':
    waiter()'''


async def waiter():
    task1 = asyncio.create_task(cook('Паста', 8))
    task2 = asyncio.create_task(cook('Салат Цезарь', 3))
    task3 = asyncio.create_task(cook('Отбивные', 16))

    await task1
    await task2
    await task3

async def cook(order, time_to_prepare):
    print(f'Новый заказ: {order}')
    await asyncio.sleep(time_to_prepare)
    print(order, '- готово')

asyncio.run(waiter())

import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor
import asyncio
from aiohttp import ClientSession
import logging
from aiogram.types import Message
from src import config

load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    '''Обработчик команды старт'''
    await message.answer(f'Привет, {message.from_user.first_name}!')

@dp.message_handler()
async def unknown_cmd(message: Message):
    '''Обработчик незнакомых команд'''
    await message.reply('Я не знаю такой команды')
@dp.message_handler(commands=['market'])
async def view_market(message: Message):
    '''Обработчик команды просмотр магазина'''
    await message.answer('Обзор магазина')

async def main():
    session = ClientSession() # Использование менеджера контекста для закрытия сессии
    bot["client_session"] = session
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        print("Polling stopped")
    finally:
        await session.close()  # Закрываем сессию в любом случае
        await bot.close()  # Закрываем бота


if __name__ == '__main__':
    if config.DEBUG:
        logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)

    # try:
    #     asyncio.run(main())
    # except KeyboardInterrupt:
    #     print('Exit')

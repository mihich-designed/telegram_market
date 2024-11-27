import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, filters
import asyncio
from aiogram.types import Message
from aiohttp import ClientSession

load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler(filters.CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!')

async def main():
    async with ClientSession() as session:  # Использование менеджера контекста
        bot["client_session"] = session
        await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

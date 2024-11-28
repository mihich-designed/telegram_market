from aiogram.types import Message, CallbackQuery
from aiogram import Bot, Dispatcher, filters
from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler(commands=['catalog'])
async def show_catalog(message: Message):
    pass



# def setup(dp: Dispatcher):
#     dp.message_handler(catalog, filters.Command("catalog"))



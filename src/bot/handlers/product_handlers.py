from aiogram.types import Message
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)





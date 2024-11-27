import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor
import asyncio
from aiohttp import ClientSession
import logging
from aiogram.types import Message
from src import config
from src.bot.keyboards.cart_keyboards import main_keyboard
# from src.bot.handlers.product_handlers import catalog
from src.database.queries import metadata, engine

load_dotenv()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)


async def on_startup(_):
    '''Запуск БД вместе с запуском бота'''
    metadata.create_all(engine)
    print('Программа успешно запущена')


@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    '''Обработчик команды старт'''
    await message.answer_sticker('CAACAgIAAxkBAANBZ0b5uy3ZDT4I3W_u9O6_KYrYMPIAAm8AA8GcYAzLDn2LwN1NVjYE')
    await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=main_keyboard)


@dp.message_handler(commands=['catalog'])
async def catalog(message: Message):
    '''Обработчик команды просмотр каталога'''
    await message.answer('Каталог')


@dp.message_handler()
async def unknown_cmd(message: Message):
    '''Обработчик незнакомых команд'''
    await message.reply('Я не знаю такой команды')


@dp.message_handler(content_types=['sticker'])
async def add_sticker(message: Message):
    '''Обработчик стикеров'''
    await message.answer(message.sticker.file_id)
    await bot.send_message(message.from_user.id, message.chat.id)


@dp.message_handler(content_types=['document', 'photo'])
async def forward_message(message: Message):
    '''Пересылка медиа от пользователей в группу'''
    await bot.forward_message(os.getenv('GROUP_ID'), message.from_user.id, message.message_id)


# @dp.message_handler(content_types=['sticker', 'photo', 'audio', 'video', 'document', 'location'])
# async def add_media(message: Message):
#     '''Обработчик медиа файлов'''
#     await bot.send_message(message.content_type.file_id, message.from_user.id, message.chat.id)

async def main():
    session = ClientSession()  # Использование менеджера контекста для закрытия сессии
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
    try:
        executor.start_polling(dp, on_startup=on_startup)
    except Exception as e:
        print(f'Ошибка: {e}')

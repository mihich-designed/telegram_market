import os
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor
import asyncio
from aiohttp import ClientSession
import logging
from aiogram.types import Message, CallbackQuery
from src import config
from src.bot.keyboards.cart_keyboards import main_keyboard
from src.database import models
from src.database import queries
from src.bot.handlers import add_product_handlers
from aiogram.dispatcher import FSMContext

load_dotenv()
storage = MemoryStorage()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    '''Запуск БД вместе с запуском бота'''
    # metadata.create_all(engine)
    try:
        models.Base.metadata.create_all(models.engine)
        print("База данных инициализирована.")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")


@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    '''Обработчик команды старт'''
    user_id = message.from_user.id
    queries.add_user(user_id)
    await message.answer_sticker('CAACAgIAAxkBAANBZ0b5uy3ZDT4I3W_u9O6_KYrYMPIAAm8AA8GcYAzLDn2LwN1NVjYE')
    await message.answer(f'Привет, {message.from_user.first_name}!', reply_markup=main_keyboard)


@dp.callback_query_handler()
async def query_callback_keyboard(callback_query: CallbackQuery):
    '''Обработчик коллбэков каталога и корзины'''
    if callback_query.data == 'catalog':

        await bot.send_message(chat_id=callback_query.from_user.id, text='Каталог')
    elif callback_query.data == 'cart':

        await bot.send_message(chat_id=callback_query.from_user.id, text='Корзина')


@dp.message_handler(content_types=['sticker'])
async def add_sticker(message: Message):
    '''Обработчик стикеров'''
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(message.sticker.file_id)
        await bot.send_message(message.from_user.id, message.chat.id)


@dp.message_handler(content_types=['document', 'photo'])
async def forward_message(message: Message):
    '''Пересылка медиа от пользователей в группу'''
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await bot.forward_message(os.getenv('GROUP_ID'), message.from_user.id, message.message_id)


class NewProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()


@dp.message_handler(commands=['add_product'])
async def add_product(message: Message):
    '''Добавление названия товара'''
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer('Напишите название товара')
        await NewProduct.next()


@dp.message_handler(state=NewProduct.name)
async def add_product_name(message: Message, state: FSMContext):
    '''Добавление описания товара и сохранение названия'''
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Укажите описание товара')
    await NewProduct.next()


@dp.message_handler(state=NewProduct.description)
async def add_product_desc(message: Message, state: FSMContext):
    '''Добавление цены товара и сохранение описания'''
    async with state.proxy() as data:
        data['description'] = message.text
    await message.answer('Укажите цену товара')
    await NewProduct.next()


@dp.message_handler(state=NewProduct.price)
async def add_product_price(message: Message, state: FSMContext):
    '''Добавление фото товара и сохранение цены'''
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Отправьте изображение товара')
    await NewProduct.next()


@dp.message_handler(lambda message: not message.photo, state=NewProduct.image)
async def check_product_image(message: Message):
    await message.reply('Это не изображение, отправьте файлы в формате .jpg или .png')


@dp.message_handler(content_types=['photo'], state=NewProduct.image)
async def add_product_image(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['image'] = message.photo[0].file_id
        queries.add_product(data['name'], data['description'], data['price'], data['image'])
    await message.answer('Товар успешно создан!')
    await state.finish()


@dp.message_handler()
async def unknown_cmd(message: Message):
    '''Обработчик незнакомых команд'''
    await message.reply('Я не знаю такой команды')


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


# handlers.setup(dp)

if __name__ == '__main__':
    if config.DEBUG:
        logging.basicConfig(level=logging.INFO)
    try:
        executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    except Exception as e:
        print(f'Ошибка: {e}')

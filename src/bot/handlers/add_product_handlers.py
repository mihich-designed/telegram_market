from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from src.main import bot, dp
import os
from dotenv import load_dotenv
from src.database import queries

load_dotenv()
class NewProduct(StatesGroup):
    name=State()
    description=State()
    price=State()
    image=State()

def register_handlers(dp):
    dp.register_message_handler(add_product, commands=['add_product'], state=None)  # Начальный обработчик
    dp.register_message_handler(add_product_name, state=NewProduct.name)
    dp.register_message_handler(add_product_desc, state=NewProduct.description)
    dp.register_message_handler(add_product_price, state=NewProduct.price)
    dp.register_message_handler(add_product_image, state=NewProduct.image)

async def add_product(message: Message, state: FSMContext):
    '''Добавление названия товара'''


# @dp.message_handler(state=NewProduct.name)
async def add_product_name(message: Message, state: FSMContext):
    '''Добавление описания товара и сохранение названия'''
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Укажите описание товара')
    await NewProduct.next()

# @dp.message_handler(state=NewProduct.description)
async def add_product_desc(message: Message, state: FSMContext):
    '''Добавление цены товара и сохранение описания'''
    async with state.proxy() as data:
        data['description'] = message.text
    await message.answer('Укажите цену товара')
    await NewProduct.next()

# @dp.message_handler(state=NewProduct.price)
async def add_product_price(message: Message, state: FSMContext):
    '''Добавление фото товара и сохранение цены'''
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Отправьте изображение товара')
    await NewProduct.next()

# @dp.message_handler(lambda message: not message.photo, state=NewProduct.image)
async def check_product_image(message: Message):
    await message.reply('Это не изображение, отправьте файлы в формате .jpg или .png')

# @dp.message_handler(content_types=['photo'], state=NewProduct.image)
async def add_product_image(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['image'] = message.photo[0].file_id
        queries.add_product(data['name'], data['description'], data['price'], data['image'])
    await message.answer('Товар успешно создан!')
    await state.finish()
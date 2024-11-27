from aiogram.types import InlineKeyboardButton
from .product_keyboards import main_keyboard

main_keyboard.add(
    InlineKeyboardButton(text='Корзина', url='https://docs.aiogram.dev/en/stable/api/session/aiohttp.html'),
)
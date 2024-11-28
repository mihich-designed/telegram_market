from aiogram.types import InlineKeyboardButton
from .product_keyboards import main_keyboard

main_keyboard.add(
    InlineKeyboardButton(text='Корзина', callback_data='cart'),
)


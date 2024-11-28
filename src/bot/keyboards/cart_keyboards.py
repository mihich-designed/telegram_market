from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .product_keyboards import main_keyboard
from src.database import models, db_session

main_keyboard.add(
    InlineKeyboardButton(text='Корзина', callback_data='cart'),
)

cart_keyboard = InlineKeyboardMarkup(row_width=1)

def create_cart_keyboard(user_id):
    with db_session.get_session() as session:
        try:
            cart = session.query(models.Cart).filter(models.Cart.user_id == user_id).all()
            if cart:
                for product in cart:
                    cart_keyboard.add(
                        InlineKeyboardButton(
                            text=f'{product} руб.', callback_data='click_product_in_cart'
                        )
                    )
        except Exception as e:
            print(f'Ошибка: {e}')
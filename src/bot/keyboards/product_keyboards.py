from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.database import models, db_session

main_keyboard = InlineKeyboardMarkup(row_width=2)

main_keyboard.add(
    InlineKeyboardButton(text='Каталог', callback_data='catalog'),
)

catalog_keyboard = InlineKeyboardMarkup(row_width=1)

with db_session.get_session() as session:
    try:
        for product in session.query(models.Product).all():
            catalog_keyboard.add(
                InlineKeyboardButton(
                    text=f'{product.name} - {product.price} руб.', callback_data='add_cart'
                )
            )
    except Exception as e:
        print(f'Ошибка: {e}')
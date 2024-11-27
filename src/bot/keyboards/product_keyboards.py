from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from src.main import main_keyboard

main_keyboard = InlineKeyboardMarkup(row_width=2)

main_keyboard.add(
    InlineKeyboardButton(text='Каталог', url='https://docs.aiogram.dev/en/stable/api/session/aiohttp.html'),
)


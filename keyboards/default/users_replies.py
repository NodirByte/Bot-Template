# import keyborads
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.db_api.connector_db import get_categories

async def categories_kb():
    categories = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=name_of_category)
        ] for name_of_category in [category.name for category in await get_categories()]
    ],
    resize_keyboard=True
    )
    return categories

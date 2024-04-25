# import inline keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.connector_db import get_child_product_by_id, get_user_by_telegram_id, user_has_reviewed_product
# from utils.db_api.connector_db import 

async def get_products_kb_in(product_id, telegram_id):
    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(
        InlineKeyboardButton(
            text="Barcha turlari",
            callback_data=f"product:{product_id}:{telegram_id}"
        )
    )    
    return inline_keyboard

async def get_child_product_kb_in(child_product_id, telegram_id):
    EXCELLENT = "A'lo"
    MEDIUM = "Yaxshi"
    BAD = "Qoniqarsiz"
    child_product = await get_child_product_by_id(child_product_id)
    user = await get_user_by_telegram_id(telegram_id)
    user_has_reviewed = await user_has_reviewed_product(user, child_product)
    if user_has_reviewed:
        return InlineKeyboardMarkup()
    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(
        InlineKeyboardButton(
            text=EXCELLENT,
            callback_data=f"rate:{child_product_id}:{EXCELLENT}:{telegram_id}"
        ),
        InlineKeyboardButton(
            text=MEDIUM,
            callback_data=f"rate:{child_product_id}:{MEDIUM}:{telegram_id}"
        ),
        InlineKeyboardButton(
            text=BAD,
            callback_data=f"rate:{child_product_id}:{BAD}:{telegram_id}"
        )
    )
    return inline_keyboard



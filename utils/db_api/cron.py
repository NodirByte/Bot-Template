import asyncio

from keyboards.inline.users_inlines import get_products_kb_in
from loader import bot
from utils.db_api.connector_db import get_sales

DAILY_CRON_INTERVAL = 5  # 1 second for testing purposes


async def ask_review_for_product():
    print("Cron started")
    while True:
        print("Cron iteration")
        await asyncio.sleep(DAILY_CRON_INTERVAL)
        sales = await get_sales()
        print(sales)
        for sale in sales:
            product, user = sale.product, sale.user
            products_kb_in = await get_products_kb_in(
                product.id, user.telegram_id, spatial="review"
            )
            file_path = product.image.path
            caption = f"{product.name}\n{product.number}"
            try:
                with open(file_path, "rb") as file:
                    await bot.send_document(
                        user.telegram_id,
                        file,
                        caption=caption,
                        reply_markup=products_kb_in,
                    )
            except Exception as e:
                print(e)
                await bot.send_message(user.telegram_id, caption)

import asyncio

from loader import bot
from utils.db_api.connector_db import (
    get_users,
    get_product_by_user,
    get_sale_by_user_product,
    get_all_containers,
)
from keyboards.inline.users_inlines import get_products_kb_in

DAILY_CRON_INTERVAL = 3 # 1 second for testing purposes


async def ask_review_for_product():
    while True:
        await asyncio.sleep(DAILY_CRON_INTERVAL)
        # Here you can perform any task you need to schedule
        all_users = await get_users()
        print("\nAll users -> ", all_users)
        all_containers = await get_all_containers()
        for user in all_users:
            print("\nUser -> ", user)
            for container in all_containers:
                print("\nContainer -> ", container)
                products = await get_product_by_user(user, container)
                print("\nProducts -> ", products)
                for product in products:
                    sale = await get_sale_by_user_product(user, product, container)
                    for s in sale:
                        print("\nSale -> ", s)
                    print("\nProduct -> ", product)
                    products_kb_in = await get_products_kb_in(product.id, user.telegram_id)
                    file_path = product.image.path
                    caption = f"{product.name}\n{product.number}"
                    try:
                        with open(file_path, "rb") as file:
                            await bot.send_document(
                                user.telegram_id, file, caption=caption, reply_markup=products_kb_in
                            )
                    except Exception as e:
                        print(e)
                        await bot.send_message(user.telegram_id, caption)

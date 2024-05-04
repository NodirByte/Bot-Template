import asyncio

from loader import bot

DAILY_CRON_INTERVAL = 60 * 60 * 24  # 24 hours in seconds


async def ask_review_for_product():
    while True:
        await asyncio.sleep(DAILY_CRON_INTERVAL)
        # Here you can perform any task you need to schedule
        # TODO: get all clients here
        # TODO: get all container
        # TODO: find products of these clients
        # TODO: send a message to each client to ask for a review
        # TODO: save review status in the database
        # after saving review, increment review count for sale.
        # asking is a kind of inline keyboard like general asking
        await bot.send_message(chat_id="821685125", text="Scheduled message")

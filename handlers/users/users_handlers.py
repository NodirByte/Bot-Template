from keyboards.inline.users_inlines import (
    get_products_kb_in,
    get_child_product_kb_in,
    get_sp_child_product_kb_in,
)
from loader import dp, bot
from aiogram import types

from utils.db_api.connector_db import (
    get_categories,
    get_child_product_by_id,
    get_products_child,
    get_products_parent,
    get_sale_by_cp_ids,
    get_user_by_telegram_id,
    rate_product,
    get_sale_by_cp_ids,
    update_review_count,
)
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext


@dp.message_handler()
async def categories(message: types.Message):
    telegram_id = message.from_user.id
    category_text = message.text.strip()

    categories_list = await get_categories()
    category_names = [category.name for category in categories_list]

    if category_text not in category_names:
        await message.answer(
            "Berilgan kategoriyada hech qanday mahsulot topilmadi! Iltimos, qaytadan urinib ko'ring!"
        )
        return

    products = await get_products_parent(category_text)

    for product in products:
        products_kb_in = await get_products_kb_in(product.id, telegram_id)
        file_path = product.image.path
        caption = f"{category_text}\n{product.name}\n{product.number}"
        try:
            with open(file_path, "rb") as file:
                await message.bot.send_document(
                    telegram_id, file, caption=caption, reply_markup=products_kb_in
                )
        except Exception as e:
            print(e)
            await message.answer(caption)


@dp.callback_query_handler(lambda query: query.data.startswith("product"), state=None)
async def product(query: CallbackQuery, state: FSMContext):
    try:
        _, product_id, telegram_id, container_id = query.data.split(":")
        print("\nData: ", query.data)
        child_products = await get_products_child(product_id)
        print("\nChild Products: ", child_products)
        for child_product in child_products:
            if container_id != "None":
                child_product_kb_in = await get_sp_child_product_kb_in(
                    child_product.id, telegram_id, container_id
                )
                print("\nInlined Keyboard: ", child_product_kb_in)
            else:
                child_product_kb_in = await get_child_product_kb_in(
                    child_product.id, telegram_id
                )
            file_path = child_product.image.path
            caption = f"{child_product.name}\n{child_product.number}"
            with open(file_path, "rb") as file:
                await query.bot.send_document(
                    telegram_id, file, caption=caption, reply_markup=child_product_kb_in
                )
    except Exception as e:

        print("Error in types of Product: ", e)
        await query.answer("Error")


@dp.callback_query_handler(lambda query: query.data.startswith("rate"), state=None)
async def rate_of_product(query: CallbackQuery, state: FSMContext):
    try:
        _, child_product_id, rating, telegram_id = query.data.split(":")
        await query.answer(f"Siz {rating}ga baholadingiz!")
        # remove inline keyboard from message
        await bot.edit_message_reply_markup(
            chat_id=telegram_id, message_id=query.message.message_id
        )
        EXCELLENT = "EXCELLENT"
        MEDIUM = "MEDIUM"
        BAD = "BAD"
        if rating == "A'lo":
            rating = EXCELLENT
        elif rating == "Yaxshi":
            rating = MEDIUM
        elif rating == "Qoniqarsiz":
            rating = BAD
        try:
            child_product = await get_child_product_by_id(child_product_id)
            user = await get_user_by_telegram_id(telegram_id)
            await rate_product(user, child_product, rating)
        except Exception as e:
            print(e)
            await query.answer("Error")

    except Exception as e:
        print(e)
        await query.answer("Error")


@dp.callback_query_handler(lambda query: query.data.startswith("review"), state=None)
async def rate_of_product(query: CallbackQuery, state: FSMContext):
    try:
        _, child_product_id, rating, telegram_id, container_id = query.data.split(":")
        await query.answer(f"Siz {rating}ga baholadingiz!")
        # remove inline keyboard from message
        await bot.edit_message_reply_markup(
            chat_id=telegram_id, message_id=query.message.message_id
        )
        EXCELLENT = "EXCELLENT"
        MEDIUM = "MEDIUM"
        BAD = "BAD"
        if rating == "A'lo":
            rating = EXCELLENT
        elif rating == "Yaxshi":
            rating = MEDIUM
        elif rating == "Qoniqarsiz":
            rating = BAD
        try:
            child_product = await get_child_product_by_id(child_product_id)
            sale = await get_sale_by_cp_ids(child_product_id, container_id)
            user = await get_user_by_telegram_id(telegram_id)
            await rate_product(user, child_product, rating, sale)
            await update_review_count(sale)
        except Exception as e:
            print(e)
            await query.answer("Error")

    except Exception as e:
        print(e)
        await query.answer("Error")

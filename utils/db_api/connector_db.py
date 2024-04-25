import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm.settings")
from django import setup

setup()
from asgiref.sync import sync_to_async
from orm_app import models
from django.core.exceptions import ObjectDoesNotExist


@sync_to_async
def get_users():
    return list(models.User.objects.all())


@sync_to_async
def get_categories():
    return list(models.Category.objects.all())


@sync_to_async
def get_user_organization(telegram_id):
    return models.User.objects.get(telegram_id=telegram_id).organization


@sync_to_async
def rate_product(user: models.User, product: models.Product, rate: str):
    try:
        review = models.Review.objects.get(user=user, product=product)
        review.rating = rate
    except models.Review.DoesNotExist:
        review = models.Review.objects.create(user=user, product=product, rating=rate)
    return review


@sync_to_async
def user_has_reviewed_product(user: models.User, product: models.Product):
    return models.Review.objects.filter(user=user, product=product).exists()


@sync_to_async
def get_user_by_telegram_id(telegram_id):
    return models.User.objects.get(telegram_id=telegram_id)


@sync_to_async
def get_child_product_by_id(child_product_id):
    return models.Product.objects.get(id=child_product_id)


@sync_to_async
def get_products_parent(category_name):
    category_id = models.Category.objects.get(name=category_name).id
    return list(models.Product.objects.filter(category_id=category_id, parent=None))


@sync_to_async
def get_products_child(product_id):
    child_products = list(models.Product.objects.filter(parent_id=product_id))
    parent_product = models.Product.objects.get(id=product_id)
    child_products.append(parent_product)
    return child_products

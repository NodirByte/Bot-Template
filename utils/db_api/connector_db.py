import os

from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm.settings")
from django import setup

setup()
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from orm_app import models


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
def rate_product(
    user: models.User, product: models.Product, rate: str, sale: models.Sale = None
):
    review, _ = models.Review.objects.update_or_create(
        user=user, product=product, rating=rate, sale=sale
    )
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
def get_sale_by_product_id(product_id):
    return models.Sale.objects.get(product_id=product_id)


@sync_to_async
def update_review_count(sale):
    sale.review_count += 1
    sale.save()


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


@sync_to_async
def get_product_by_user(user, container) -> list[models.Product]:
    product_ids = models.Sale.objects.filter(
        user=user, container=container, review_count__lt=settings.REVIEW_LIMIT
    ).values_list("product_id", flat=True)
    return list(models.Product.objects.filter(id__in=product_ids))


@sync_to_async
def get_sales():
    # due_date = timezone.now() - timezone.timedelta(days=settings.REVIEW_DAYS)
    return list(
        models.Sale.objects.filter(
            review_count__lt=settings.REVIEW_LIMIT,
            # purchase_date__lte=due_date,
        ).select_related("product", "user")
    )


@sync_to_async
def get_all_containers():
    return list(models.Container.objects.all())

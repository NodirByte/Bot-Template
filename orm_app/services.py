from django.db.models import OuterRef, Subquery, Count

from .models import Review, Sale, Product, Container


def review():

    # bad_reviews_subquery = (
    #     Review.objects.filter(sale=OuterRef("pk"), rating=Review.BAD)
    #     .values("sale")
    #     .annotate(bad_reviews=Count("pk"))
    #     .values("bad_reviews")
    # )
    # by product and sale
    bad_reviews_subquery = (
        Review.objects.filter(sale=OuterRef("pk"), rating=Review.BAD)
        .values("sale", "product")
        .annotate(bad_reviews=Count("pk"))
        .values("bad_reviews")
    )

    # medium_reviews_subquery = (
    #     Review.objects.filter(sale=OuterRef("pk"), rating=Review.MEDIUM)
    #     .values("sale")
    #     .annotate(medium_reviews=Count("pk"))
    #     .values("medium_reviews")
    # )

    # excellent_reviews_subquery = (
    #     Review.objects.filter(sale=OuterRef("pk"), rating=Review.EXCELLENT)
    #     .values("sale")
    #     .annotate(excellent_reviews=Count("pk"))
    #     .values("excellent_reviews")
    # )
    # by product and sale
    medium_reviews_subquery = (
        Review.objects.filter(sale=OuterRef("pk"), rating=Review.MEDIUM)
        .values("sale", "product")
        .annotate(medium_reviews=Count("pk"))
        .values("medium_reviews")
    )

    excellent_reviews_subquery = (
        Review.objects.filter(sale=OuterRef("pk"), rating=Review.EXCELLENT)
        .values("sale", "product")
        .annotate(excellent_reviews=Count("pk"))
        .values("excellent_reviews")
    )

    sales = Sale.objects.annotate(
        bad_reviews=Subquery(bad_reviews_subquery),
        medium_reviews=Subquery(medium_reviews_subquery),
        excellent_reviews=Subquery(excellent_reviews_subquery),
    )

    for sale in sales:
        print(
            f"Sale: {sale.id}, Bad Reviews: {sale.bad_reviews}, Medium Reviews: {sale.medium_reviews}, Excellent Reviews: {sale.excellent_reviews}"
        )


def review_gpt():
    from django.db.models import Count, Q

    # Define your queryset to get the statistics
    container_stats = Container.objects.annotate(
        excellent_reviews=Count(
            "sale__review", filter=Q(sale__review__rating=Review.EXCELLENT)
        ),
        medium_reviews=Count(
            "sale__review", filter=Q(sale__review__rating=Review.MEDIUM)
        ),
        bad_reviews=Count("sale__review", filter=Q(sale__review__rating=Review.BAD)),
    ).values(
        "number",
        "excellent_reviews",
        "medium_reviews",
        "bad_reviews",
        "sale__product__name",
        "sale__review__user__name",
    )

    # Print the statistics
    for stat in container_stats:
        print(f"Container: {stat['number']}, Product: {stat['sale__product__name']}")
        print(f"Excellent Reviews: {stat['excellent_reviews']}")
        print(f"Medium Reviews: {stat['medium_reviews']}")
        print(f"Bad Reviews: {stat['bad_reviews']}")
        print(f"Reviewers: {stat['sale__review__user__name']}")
        print("--------------------------------------")

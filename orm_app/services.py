from collections import defaultdict

from django.db.models import Count, OuterRef, Subquery

from .models import Container, Product, Review, Sale, User

# def review():

#     # bad_reviews_subquery = (
#     #     Review.objects.filter(sale=OuterRef("pk"), rating=Review.BAD)
#     #     .values("sale")
#     #     .annotate(bad_reviews=Count("pk"))
#     #     .values("bad_reviews")
#     # )
#     # by product and sale
#     bad_reviews_subquery = (
#         Review.objects.filter(sale=OuterRef("pk"), rating=Review.BAD)
#         .values("sale", "product")
#         .annotate(bad_reviews=Count("pk"))
#         .values("bad_reviews")
#     )

#     # medium_reviews_subquery = (
#     #     Review.objects.filter(sale=OuterRef("pk"), rating=Review.MEDIUM)
#     #     .values("sale")
#     #     .annotate(medium_reviews=Count("pk"))
#     #     .values("medium_reviews")
#     # )

#     # excellent_reviews_subquery = (
#     #     Review.objects.filter(sale=OuterRef("pk"), rating=Review.EXCELLENT)
#     #     .values("sale")
#     #     .annotate(excellent_reviews=Count("pk"))
#     #     .values("excellent_reviews")
#     # )
#     # by product and sale
#     medium_reviews_subquery = (
#         Review.objects.filter(sale=OuterRef("pk"), rating=Review.MEDIUM)
#         .values("sale", "product")
#         .annotate(medium_reviews=Count("pk"))
#         .values("medium_reviews")
#     )

#     excellent_reviews_subquery = (
#         Review.objects.filter(sale=OuterRef("pk"), rating=Review.EXCELLENT)
#         .values("sale", "product")
#         .annotate(excellent_reviews=Count("pk"))
#         .values("excellent_reviews")
#     )

#     sales = Sale.objects.annotate(
#         bad_reviews=Subquery(bad_reviews_subquery),
#         medium_reviews=Subquery(medium_reviews_subquery),
#         excellent_reviews=Subquery(excellent_reviews_subquery),
#     )

#     for sale in sales:
#         print(
#             f"Sale: {sale.id}, Bad Reviews: {sale.bad_reviews}, Medium Reviews: {sale.medium_reviews}, Excellent Reviews: {sale.excellent_reviews}"
#         )


# def review_gpt():
#     from django.db.models import Count, Q

#     # Define your queryset to get the statistics
#     container_stats = Container.objects.annotate(
#         excellent_reviews=Count(
#             "sale__review", filter=Q(sale__review__rating=Review.EXCELLENT)
#         ),
#         medium_reviews=Count(
#             "sale__review", filter=Q(sale__review__rating=Review.MEDIUM)
#         ),
#         bad_reviews=Count("sale__review", filter=Q(sale__review__rating=Review.BAD)),
#     ).values(
#         "number",
#         "excellent_reviews",
#         "medium_reviews",
#         "bad_reviews",
#         "sale__product__name",
#         "sale__review__user__name",
#     )

#     # Print the statistics
#     for stat in container_stats:
#         print(f"Container: {stat['number']}, Product: {stat['sale__product__name']}")
#         print(f"Excellent Reviews: {stat['excellent_reviews']}")
#         print(f"Medium Reviews: {stat['medium_reviews']}")
#         print(f"Bad Reviews: {stat['bad_reviews']}")
#         print(f"Reviewers: {stat['sale__review__user__name']}")
#         print("--------------------------------------")


# def get_review_statistics(container_id):
#     review_statistics = {}

#     # Retrieve all products in the specified container
#     products = Product.objects.filter(sale__container__id=container_id).distinct()

#     # Iterate over each product to get review statistics
#     for product in products:
#         # Fetch review counts for each rating category
#         review_counts = (
#             Review.objects.filter(product=product)
#             .values("rating")
#             .annotate(count=Count("rating"))
#         )

#         # Fetch users who gave reviews for this product
#         reviewers = (
#             User.objects.filter(review__product=product)
#             .distinct()
#             .values_list("name", flat=True)
#         )

#         # Store review statistics in the dictionary
#         review_statistics[product.name] = {
#             "reviews": {
#                 review_count["rating"]: review_count["count"]
#                 for review_count in review_counts
#             },
#             "reviewers": list(reviewers),
#         }

#     return review_statistics


def get_review_statistics_by_container(container_id):
    review_statistics = {}

    # Retrieve all products in the specified container
    products = Product.objects.filter(sale__container__id=container_id).distinct()

    # Iterate over each product to get review statistics
    for product in products:
        # Fetch review counts for each rating category
        review_counts = (
            Review.objects.filter(product=product)
            .values("rating")
            .annotate(count=Count("rating"))
        )

        # Fetch users who gave reviews for this product
        reviewers = User.objects.filter(review__product=product).distinct()

        # Initialize a dictionary to store reviewer information
        reviewers_info = defaultdict(list)

        # Iterate over each reviewer to get their reviews for this product
        for reviewer in reviewers:
            reviews_by_reviewer = Review.objects.filter(product=product, user=reviewer)
            for review in reviews_by_reviewer:
                reviewers_info[reviewer.name].append(review.rating)

        # Store review statistics and reviewer information in the dictionary
        review_statistics[product.name] = {
            "reviews": {
                review_count["rating"]: review_count["count"]
                for review_count in review_counts
            },
            "reviewers": {
                reviewer.name: reviewers_info[reviewer.name] for reviewer in reviewers
            },
        }

    return review_statistics

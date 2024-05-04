from django.shortcuts import render

from .models import Product, Review


def product_ratings_view(request):
    # Get all parent products (products with no parent)
    parent_products = Product.objects.filter(parent=None)

    products_with_ratings = []
    for parent in parent_products:
        # Get all child products of the current parent
        child_products = list(parent.product_set.all())
        parent_product = parent
        child_products.append(parent_product)

        # Get parent's average rating
        parent_rating = calculate_average_rating(parent.review_set.all())

        # Prepare data for child products
        child_products_with_ratings = []
        for child in child_products:
            child_reviews = Review.objects.filter(product=child)
            child_rating = calculate_average_rating(child_reviews)
            child_products_with_ratings.append(
                {
                    "child_product": child,
                    "child_rating": child_rating,
                    "child_reviews": child_reviews,
                }
            )

        # Append data to the main list
        products_with_ratings.append(
            {
                "parent_product": parent,
                "parent_rating": parent_rating,
                "child_products_with_ratings": child_products_with_ratings,
            }
        )

    context = {"products_with_ratings": products_with_ratings}

    return render(request, "layout/index.html", context)


def calculate_average_rating(reviews):
    if reviews.exists():
        total_ratings = sum(get_numeric_rating(review.rating) for review in reviews)
        return round(total_ratings / len(reviews), 2)  # Round to 2 decimal places
    return 0


def get_numeric_rating(rating_str):
    if rating_str == Review.EXCELLENT:
        return 5  # Example: Mapping "EXCELLENT" to numeric value (e.g., 5)
    elif rating_str == Review.MEDIUM:
        return 3  # Example: Mapping "MEDIUM" to numeric value (e.g., 3)
    elif rating_str == Review.BAD:
        return 1  # Example: Mapping "BAD" to numeric value (e.g., 1)
    else:
        return 0  # Default value if no match

from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100)
    telegram_id = models.IntegerField()
    phone_number = models.CharField(max_length=100, null=False, blank=False)
    organization = models.ForeignKey(
        "Organization", on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    organization = models.ForeignKey(
        "Organization", on_delete=models.SET_NULL, null=True, blank=True
    )
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Container(models.Model):
    number = models.CharField(max_length=100)
    arrival_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.number


class Sale(models.Model):
    user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, blank=True
    )
    container = models.ForeignKey(
        "Container", on_delete=models.SET_NULL, null=True, blank=True
    )
    purchase_date = models.DateField()
    review_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return (
            self.product.name + " - " + str(self.purchase_date) + " - " + self.user.name
        )


class Review(models.Model):
    EXCELLENT = "EXCELLENT"
    MEDIUM = "MEDIUM"
    BAD = "BAD"
    RATING_CHOICES = [
        (EXCELLENT, "Excellent"),
        (MEDIUM, "Medium"),
        (BAD, "Bad"),
    ]
    user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, blank=True
    )
    rating = models.CharField(max_length=100, choices=RATING_CHOICES)
    sale = models.ForeignKey("Sale", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.rating + " - " + self.product.name + " - " + self.user.name


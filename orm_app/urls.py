from django.urls import path
from .views import product_ratings_view

urlpatterns = [
    path('data/', product_ratings_view, name='data_display'),
]

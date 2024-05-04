from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='containers_list'),
    path('container/<int:container_id>/', views.container_detail, name='container_detail'),
    # path('reviewer_detail/<str:reviewer_name>/', views.reviewer_detail, name='reviewer_detail'),
]

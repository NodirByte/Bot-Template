from django.urls import path
from .views import IndexView, ContainerDetailView


urlpatterns = [
    path('', IndexView.as_view(), name='containers_list'),
    path('detail/<int:pk>/', ContainerDetailView.as_view(), name='container-detail'),
]
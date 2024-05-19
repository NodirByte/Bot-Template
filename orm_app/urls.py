from django.urls import path
from .views import IndexView, ContainerDetailView, ReviewersView, ReviewerDetailView, ProductsStatisticsView


urlpatterns = [
    path("", IndexView.as_view(), name="containers_list"),
    path("c-detail/<int:pk>/", ContainerDetailView.as_view(), name="container-detail"),
    path("reviewers/", ReviewersView.as_view(), name="reviewers"),
    path("r-detail/<int:pk>/", ReviewerDetailView.as_view(), name="reviewer-detail"),
    path("pdts-st/<str:from_date>_<str:to_date>/", ProductsStatisticsView.as_view(), name="products-statistics"),]

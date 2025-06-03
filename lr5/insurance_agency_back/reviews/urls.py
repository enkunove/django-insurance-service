from django.urls import path
from . import views
from .views import ReviewCreateView, ReviewListView

urlpatterns = [
    path('', views.review, name="reviews"),
    path('me/', ReviewListView.as_view(), name="my-reviews"),
    path('add/', ReviewCreateView.as_view(), name="review-add"),
]
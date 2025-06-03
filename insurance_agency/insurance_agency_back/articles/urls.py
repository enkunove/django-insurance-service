from django.urls import path
from . import views


urlpatterns = [
    path('news/', views.news, name='news'),
    path('<int:pk>/', views.article, name='article'),
]
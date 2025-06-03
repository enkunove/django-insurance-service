from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('contacts/', views.contacts, name='contacts'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('register/', views.register, name='registration'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('statistics/', views.statistics, name='statistics')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
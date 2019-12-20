from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='community-homepage'),
    path('search/', views.searchpage, name='community-search'),
    path('profile/', views.profilepage, name='community-profile'),
]
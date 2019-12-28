from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='chat-homepage'),
    path('<str:room_name>/', views.room, name='room'),
]
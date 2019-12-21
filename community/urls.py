from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='community-homepage'),
    path('search/', views.searchpage, name='community-search'),
    path('profile/', views.profilepage, name='community-profile'),
    path('profile/edit/', views.editprofilepage, name='community-profile-edit'),
    path('discussions/', views.alldiscussionspage, name='community-discussions'),
    path('discussions/new/', views.newdiscussionpage, name='community-discussions-new'),
    path('discussions/<slug:username>', views.mydiscussionpage, name='community-discussions-user'),
]
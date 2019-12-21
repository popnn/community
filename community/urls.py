from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='community-homepage'),
    path('search/', views.searchpage, name='community-search'),
    path('signup/', views.signuppage, name='community-signup'),
    path('profile/', views.profilepage, name='community-profile'),
    path('profile/edit/', views.editprofilepage, name='community-profile-edit'),
    path('discussions/', views.alldiscussionspage, name='community-discussions'),
    path('new-discussion/', views.newdiscussionpage, name='community-discussions-new'),
    path('discussions/<slug:username>/', views.mydiscussionpage, name='community-discussions-user'),
    path('discussions/<slug:username>/<int:discussion_id>/', views.selectdiscussionpage, name='community-discussions-single'),
]
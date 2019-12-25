from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='community-homepage'),
    path('search/', views.searchpage, name='community-search'),
    path('signup/', views.signuppage, name='community-signup'),
    path('profile/', views.profilepage, name='community-profile'),
    path('profile/view/<slug:username>/', views.viewprofilepage, name='community-profile'),
    path('profile/edit/', views.editprofilepage, name='community-profile-edit'),
    path('new-conversation/<int:other_user_id>/', views.newconversationpage, name='community-new-conversations'),
    path('conversations/', views.allconversationspages, name='community-all-conversations'),
    path('conversations/<int:conversation_id>/', views.selectconversationpage, name='community-select-conversation'),
    path('new-discussion/', views.newdiscussionpage, name='community-discussions-new'),
    path('discussions/', views.alldiscussionspage, name='community-discussions'),
    path('discussions/<slug:username>/', views.mydiscussionpage, name='community-discussions-user'),
    path('discussions/<slug:username>/<int:discussion_id>/', views.selectdiscussionpage, name='community-discussions-single'),
    path('edit-discussion/<slug:username>/<int:discussion_id>/', views.editdiscussionpage, name='community-edit-discussion-single'),
    path('ajax-serverside-query/', views.ajax_response, name='ajax-response'),
]
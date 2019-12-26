"""popN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import settings

def logout_function(request):
    logout(request)
    response = redirect("/")
    if request.COOKIES.get('id', None) is not None:
        response.delete_cookie('id')
    return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', logout_function, name='logout'),
    path('', include('community.urls'), name='community'),
    path('', include('pwa_webpush.urls')),
    #password Reset
    path('reset-password/',
         auth_views.PasswordResetView.as_view(
            template_name = 'passReset/password_reset_form.html',
            subject_template_name='passReset/password_reset_subject.txt',
            email_template_name='passReset/password_reset_email.html',
            success_url='/login/'
        ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='passReset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='passReset/password_reset_confirm.html'
         ),
        name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='passReset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
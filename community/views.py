from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from PIL import Image
from .models import *
from .forms import *
import json
import os
from popN.settings import BASE_DIR 

def verify_request(request):
    return request.COOKIES.get('id', None) is not None, request.COOKIES.get('id', None)

def render_template(request, template_name, context={}):
    response = render(request, template_name, context)
    return response

# Create your views here.
def homepage(request):
    logged_in, user_id = verify_request(request)
    if logged_in:
        context = {
            'title': "Home",
            'logged_in': logged_in,
            "all_cards": [],
        }
        for card_no in range(15):
            cnt = {
                'card_title': 'Sample Card #{}'.format(card_no),
                'card_text': ' Sample text: Welcom to popN Community, The one stop for all thats popN ;)',
            }
            context['all_cards'].append(cnt)
        return render_template(request, 'community/homepage.html', context)
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    response = redirect('/community')
                    user_id = UserProfiles.objects.get(username=username).user_id
                    response.set_cookie('id', user_id)
                    return response 
        else:
            form = AuthenticationForm()
        return render_template(request, 'community/previewpage.html', {'form': form})

def searchpage(request):
    logged_in, user_id = verify_request(request)
    if request.method == 'GET':
        query = request.GET.get('q', None)
    context = {
        'title': 'Search-{}'.format(query) if query is not None else 'Search',
        'query': query,
        'logged_in': logged_in,
    }
    
    if query is not None:
        context['search_results'] = search(query, logged_in)
    return render_template(request, 'community/searchpage.html', context)

def profilepage(request):
    logged_in, user_id = verify_request(request)
    if not logged_in:
        return redirect('/')
    else:
        user_data = UserProfiles.objects.get(user_id=user_id)
        user_data_main = User.objects.get(username=user_data.username)
        print(user_data.user_following)
        context = {
            'title': 'Profile',
            'logged_in': logged_in,
            'image_path': user_data.user_profile_image,
            'first_name': user_data_main.first_name,
            'last_name': user_data_main.last_name,
            'username': user_data.username,
            'email': user_data_main.email,
            'description': user_data.user_description,
            'followers': sum(1 for val in UserProfiles.objects.all() if str(user_data.user_id) in val.user_following.split(", ")),
            'followed_threads': [ CommunityDiscussions.objects.get(discussion_id=int(val)).discussion_title for val in user_data.user_threads.split(", ") if val != ""],
            'profile_image': user_data.user_profile_image.url,
        }
        return render_template(request, 'community/profilepage.html', context)

def editprofilepage(request):
    logged_in, user_id = verify_request(request)
    if not logged_in:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, request.FILES)
            if form.is_valid():
                user_data = UserProfiles.objects.get(user_id=user_id)
                user_data_main = User.objects.get(username=user_data.username)
                user_data_main.first_name = form.cleaned_data.get('first_name')
                user_data_main.last_name = form.cleaned_data.get('last_name')
                user_data_main.email = form.cleaned_data.get('email')
                user_data.user_description = form.cleaned_data.get('description')
                user_data.user_profile_image = form.cleaned_data.get('profile_image')
                user_data.save()
                user_data_main.save()
                return redirect('/community/profile/')
        form = EditProfileForm()
        return render_template(request, 'community/editprofilepage.html', {"form":form})

def search(query, logged_in):
    pass

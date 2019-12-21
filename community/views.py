from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
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
        for card in CommunityDiscussions.objects.all():
            cnt = {
                'card_title': card.discussion_title,
                'card_text': card.discussion_description,
                'card_url': "/discussions/{}/{}/".format(UserProfiles.objects.get(user_id=card.discussion_author_id).username, card.discussion_id),
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
                    response = redirect('/')
                    user_id = UserProfiles.objects.get(username=username).user_id
                    response.set_cookie('id', user_id)
                    return response 
        else:
            form = AuthenticationForm()
        return render_template(request, 'community/previewpage.html', {'form': form})

def signuppage(request):
    logged_in, user_id = verify_request(request)
    if logged_in:
        return redirect("/")
    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                password_verify = form.cleaned_data.get('password_verify')
                email = form.cleaned_data.get('email')
                if username not in [user.username for user in User.objects.all()] and str(password)==str(password_verify):
                    User.objects.create_user(username=username, password=password, email=email).save()
                    UserProfiles(username=username).save()
                    Email_content="Dear " + username + ",\n\nYour user is successfully created with username " + username + " Logon to popn.ml to access your account.\n\n For support email us support@popn.ml\n\nThank You\n\nTeam popN" 
                    email_message = EmailMessage('popN - User Created', Email_content, to=[email])
                    email_message.send()
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    response = redirect("/profile/edit")
                    user_id = UserProfiles.objects.get(username=username).user_id
                    response.set_cookie('id', user_id)
                    return response 
        else:
            form = CreateUserForm()
        return render_template(request, 'community/signuppage.html', {'form': form})

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
        followers_count = sum(1 for val in UserProfiles.objects.all() if str(user_data.user_id) in val.user_following.split(", "))
        following_users = [UserProfiles.objects.get(user_id=int(f_id)).username for f_id in user_data.user_following.split(", ") if f_id != '']
        my_threads = [val.discussion_title for val in CommunityDiscussions.objects.filter(discussion_author_id=user_id)]
        context = {
            'title': 'Profile',
            'logged_in': logged_in,
            'first_name': user_data_main.first_name,
            'last_name': user_data_main.last_name,
            'username': user_data.username,
            'email': user_data_main.email,
            'description': user_data.user_description,
            'followers_count': followers_count,
            'following_users': following_users,
            'following_users_count': len(following_users),
            'profile_image': user_data.user_profile_image.url,
            'my_threads': my_threads,
            'my_threads_count': len(my_threads),
        }
        return render_template(request, 'community/profilepage.html', context)

def viewprofilepage(request, username):
    logged_in, user_id = verify_request(request)
    if not logged_in:
        return redirect('/')
    elif str(username) == str(UserProfiles.objects.get(user_id=user_id).username):
        return redirect('/profile/')
    else:
        if request.method == "POST":
            if request.POST.get("follow"):
                user_obj = UserProfiles.objects.get(user_id=user_id)
                user_obj.user_following = ", ".join(user_obj.user_following.split(", ") + [str(UserProfiles.objects.get(username=username).user_id)])
                user_obj.save()
            elif request.POST.get("unfollow"):
                user_obj = UserProfiles.objects.get(user_id=user_id)
                base = user_obj.user_following.split(", ")
                base.remove(str(UserProfiles.objects.get(username=username).user_id))
                user_obj.user_following = ", ".join(base)
                user_obj.save()
        user_data = UserProfiles.objects.get(user_id=UserProfiles.objects.get(username=username).user_id)
        user_data_main = User.objects.get(username=username)
        context = {
            "following": str(UserProfiles.objects.get(username=username).user_id) in UserProfiles.objects.get(user_id=user_id).user_following.split(", "),
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
        return render_template(request, 'community/viewprofilepage.html', context)


def editprofilepage(request):
    logged_in, user_id = verify_request(request)
    if not logged_in:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, request.FILES)
            if form.is_valid():
                email_address = User.objects.get(username=UserProfiles.objects.get(user_id=user_id).username).email
                user_data = UserProfiles.objects.get(user_id=user_id)
                user_data_main = User.objects.get(username=user_data.username)
                user_data_main.first_name = form.cleaned_data.get('first_name')
                user_data_main.last_name = form.cleaned_data.get('last_name')
                user_data_main.email = form.cleaned_data.get('email')
                user_data.user_description = form.cleaned_data.get('description')
                img = form.cleaned_data.get('profile_image')
                if img:
                    user_data.user_profile_image = img
                user_data.save()
                user_data_main.save()
                email_text = 'popN - Profile Updated', 'Dear {},\n\n Your profile has been updated.\n\nThank You\n\nTeam popN'.format(user_data_main.first_name)
                EmailMessage(email_text, to=[email_address]).send()
                return redirect('/profile/')
        user_data = UserProfiles.objects.get(user_id=user_id)
        user_data_main = User.objects.get(username=user_data.username)
        form = EditProfileForm({
            'first_name': user_data_main.first_name,
            'last_name': user_data_main.last_name,
            'email': user_data_main.email,
            'description': user_data.user_description,
            'profile_image': user_data.user_profile_image,
        })
        
        return render_template(request, 'community/editprofilepage.html', {"form":form})

def selectdiscussionpage(request, username, discussion_id):
    logged_in, user_id = verify_request(request)
    if not logged_in:
        return redirect('/')
    else:
        discussion = CommunityDiscussions.objects.get(discussion_id=discussion_id)
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                desc = form.cleaned_data.get('comment')
                comment = CommunityComments(
                    discussion_id=discussion_id,
                    comment_author_id=user_id,
                    comment_description=desc
                )
                comment.save()
        
        context = {
            'logged_in': logged_in,
            "title": discussion.discussion_title,
            "author": UserProfiles.objects.get(user_id=discussion.discussion_author_id).username,
            "content": discussion.discussion_description,
            "editable": discussion.discussion_author_id==user_id,
            "closed": CommunityComments.objects.filter(discussion_id=discussion.discussion_id).count() >= discussion.discussion_maximum_comments,
            "date": discussion.discussion_publish_date,
            "form": CommentForm(),
            "comments": [],
        }
        for comment in CommunityComments.objects.filter(discussion_id=discussion_id):
            context["comments"].append({
                "author": UserProfiles.objects.get(user_id=comment.comment_author_id).username,
                "description": comment.comment_description,
                "pub_date": comment.comment_publish_date,
            })
        return render_template(request, "community/singlediscussionpage.html", context)

def alldiscussionspage(request):
    logged_in, user_id = verify_request(request)
    if not logged_in:
        return redirect('/')
    else:
        context = {
            'title': "Discussions",
            'logged_in': logged_in,
            "all_cards": [],
        }
        for card in CommunityDiscussions.objects.all():
            cnt = {
                'card_title': card.discussion_title,
                'card_text': card.discussion_description,
            }
            context['all_cards'].append(cnt)
        return render_template(request, 'community/homepage.html', context)

def mydiscussionpage(request, username):
    logged_in, user_id = verify_request(request)
    if not logged_in:
        return redirect('/')
    else:
        context = {
            'title': "Discussions",
            'logged_in': logged_in,
            "all_cards": [],
        }
        for card in CommunityDiscussions.objects.filter(discussion_author_id=UserProfiles.objects.get(username=username).user_id):
            cnt = {
                'card_title': card.discussion_title,
                'card_text': card.discussion_description,
            }
            context['all_cards'].append(cnt)
        return render_template(request, 'community/homepage.html', context)
    
def newdiscussionpage(request):
    logged_in, user_id = verify_request(request)
    if not logged_in:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = DiscussionForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                description = form.cleaned_data.get('description')
                max_comments = form.cleaned_data.get('max_comments')
                description = form.cleaned_data.get('description')
                discussion = CommunityDiscussions(
                    discussion_title=title,
                    discussion_description=description,
                    discussion_maximum_comments=max_comments,
                    discussion_type="OPEN",
                    discussion_author_id=str(user_id))
                discussion.save()
                return redirect('/')
        form = DiscussionForm()
        return render_template(request, 'community/newdiscussionpage.html', {"title":"New Discussion", "form":form})

def search(query, logged_in):
    res = {
        "threads":[],
    }
    for thread in CommunityDiscussions.objects.all():
        for data in [thread.discussion_title, thread.discussion_description]:
            if query.lower() in data.lower():
                break
        else:
            continue
        res["threads"].append({
            'card_title': thread.discussion_title,
            'card_text': thread.discussion_description,
        })
    return res["threads"]

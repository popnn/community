from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from PIL import Image
from .models import *
from .forms import *
import json
import os
from popN.settings import BASE_DIR 
import datetime
import re
from tracking_analyzer.models import Tracker

#TODO Account_status 
 
def verify_request(request):
    return request.COOKIES.get('id', None) is not None, request.COOKIES.get('id', None)

def render_template(request, template_name, context={}):
    response = render(request, template_name, context)
    response.set_cookie('load', datetime.datetime.now().strftime("%H:%M:%S.%f %b %d %Y"))
    return response

@csrf_exempt
def ajax_response(request):
    if request.method=="POST":
        mode = str(request.POST.get('action'))
        if mode == 'conversation-reload':
            conv_id = int(request.POST.get('conversation_id'))
            outbox = []
            for msg_id in Conversations.objects.get(conversation_id=int(conv_id)).conversation_history.split(","):
                if msg_id != '':
                    msg = ConversationMessages.objects.get(message_id=int(msg_id))
                    time_dif = (datetime.datetime.now(datetime.timezone.utc) - msg.message_time).seconds 
                    if time_dif < 3 and request.COOKIES.get('id', None) != msg.user_id:
                        line = '<p><div class="row"><div class="col-8"><b>{} :</b> {}</div><div class="col"><small class="text-secondary">{}</small></div></div></p>'.format(UserProfiles.objects.get(user_id=msg.user_id).username, msg.message_text, msg.message_time.strftime('%b. %d,%Y, %H:%M%Z%z'))
                        outbox.append(line)
            result = {"new_data":outbox}
            response = JsonResponse(result)
            response.set_cookie('load', datetime.datetime.now().strftime("%H:%M:%S.%f %b %d %Y"))
            return response
        elif mode == 'new-conversation':
            pass
        elif mode == "delete-discussion":
            discussion_id = int(request.POST.get('discussion_id'))
            CommunityDiscussions.objects.get(discussion_id=discussion_id).delete()
            result = {"new_url":"/"}
            return JsonResponse(result)
        elif mode == "autcomplete-search":
            pass
        elif mode == "autocomplete-username":
            query, *exists = request.POST.get("query").lower().strip().split(",")[::-1]
            raw_res = []
            for f_id in UserProfiles.objects.get(user_id=int(request.COOKIES.get('id'))).user_following.split(","):
                if len(raw_res) == 3:
                    break
                if f_id.strip() != '' and int(f_id) != int(request.COOKIES.get('id')):
                    username = UserProfiles.objects.get(user_id=int(f_id.strip())).username
                    if query in username.lower() and username.lower() not in exists:
                        raw_res.append('<option value="{}">'.format(username))
            result = {"res": "\n".join(raw_res)}
            return JsonResponse(result)

# Create your views here.
def homepage(request):
    logged_in, user_id = verify_request(request)
    for usr in UserProfiles.objects.all():
        usr.user_following = ",".join([str(i).strip() for i in list(set(usr.user_following.split(","))) if str(i) != ''])
        usr.save()
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
        username = UserProfiles.objects.get(user_id=user_id).username
        user = User.objects.get(username=username)
        Tracker.objects.create_from_request(request, user)
        return render_template(request, 'community/homepage.html', context)
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username').lower()
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    response = redirect('/')
                    user_id = UserProfiles.objects.get(username=username).user_id
                    response.set_cookie('id', user_id)
                    return response 
                else:
                    messages.warning(request, 'Incorrect username/password.')
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
                username = form.cleaned_data.get('username').lower()
                password = form.cleaned_data.get('password')
                password_verify = form.cleaned_data.get('password_verify')
                email = form.cleaned_data.get('email')
                if username not in [user.username for user in User.objects.all()] and str(password)==str(password_verify):
                    User.objects.create_user(username=username, password=password, email=email).save()
                    UserProfiles(username=username).save()
                    #Email_content="Dear " + username + ",\n\nYour user is successfully created with username " + username + " Logon to popn.ml to access your account.\n\n For support email us support@popn.ml\n\nThank You\n\nTeam popN" 
                    subject="popN - Profile created"
                    html_body = render_to_string("email-template/user_created.html",{'username':username})
                    #email_message = EmailMessage('popN - User Created', Email_content, to=[email])
                    msg = EmailMultiAlternatives(subject=subject,to=[email])
                    msg.attach_alternative(html_body, "text/html")
                    msg.send()
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
        'title': 'Search-{}'.format(query) if (query is not None and len(query) > 0) else 'Search',
        'query': query,
        'logged_in': logged_in,
    }
    if query is not None and len(query) > 0:
        context['search_results'] = search(query, logged_in)
    return render_template(request, 'community/searchpage.html', context)

def profilepage(request):
    logged_in, user_id = verify_request(request)
    if not logged_in:
        return redirect('/')
    else:
        user_data = UserProfiles.objects.get(user_id=user_id)
        user_data_main = User.objects.get(username=user_data.username)
        followers = [val.username for val in UserProfiles.objects.all() if str(user_data.user_id) in val.user_following.split(",")]
        following_users = [UserProfiles.objects.get(user_id=int(f_id)).username for f_id in user_data.user_following.split(",") if f_id != '']
        user_threads = [{"title":val.discussion_title, "url":"/discussions/{}/{}".format(UserProfiles.objects.get(user_id=int(val.discussion_author_id)).username, val.discussion_id)} for val in CommunityDiscussions.objects.filter(discussion_author_id=user_data.user_id)]
        saved_threads_ids = [CommunityDiscussions.objects.get(discussion_id=int(discussion_id)) for discussion_id in user_data.user_saved_threads.split(",") if discussion_id != '']
        saved_threads = [{"title":val.discussion_title, "url":"/discussions/{}/{}".format(UserProfiles.objects.get(user_id=int(val.discussion_author_id)).username, val.discussion_id)} for val in saved_threads_ids]
        context = {
            'title': 'Profile',
            'logged_in': logged_in,
            'first_name': user_data_main.first_name,
            'last_name': user_data_main.last_name,
            'username': user_data.username,
            'email': user_data_main.email,
            'description': user_data.user_description,
            "followers": followers,
            'followers_count': len(followers),
            'following_users': following_users,
            'following_users_count': len(following_users),
            'profile_image': user_data.user_profile_image.url,
            'my_threads': user_threads,
            'my_threads_count': len(user_threads),
            'saved_threads': saved_threads,
            'saved_threads_count': len(saved_threads),
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
                user_obj.user_following = ",".join(user_obj.user_following.split(",") + [str(UserProfiles.objects.get(username=username).user_id)])
                user_obj.save()
            elif request.POST.get("unfollow"):
                user_obj = UserProfiles.objects.get(user_id=user_id)
                base = user_obj.user_following.split(",")
                base.remove(str(UserProfiles.objects.get(username=username).user_id))
                user_obj.user_following = ",".join(base)
                user_obj.save()
        user_data = UserProfiles.objects.get(user_id=UserProfiles.objects.get(username=username).user_id)
        user_data_main = User.objects.get(username=username)
        followers = [val.username for val in UserProfiles.objects.all() if str(user_data.user_id) in val.user_following.split(",")]
        following_users = [UserProfiles.objects.get(user_id=int(f_id)).username for f_id in user_data.user_following.split(",") if f_id != '']
        user_threads = [{"title":val.discussion_title, "url":"/discussions/{}/{}".format(UserProfiles.objects.get(user_id=int(val.discussion_author_id)).username, val.discussion_id)} for val in CommunityDiscussions.objects.filter(discussion_author_id=user_data.user_id)]
        saved_threads_ids = [CommunityDiscussions.objects.get(discussion_id=int(discussion_id)) for discussion_id in user_data.user_saved_threads.split(",") if discussion_id != '']
        saved_threads = [{"title":val.discussion_title, "url":"/discussions/{}/{}".format(UserProfiles.objects.get(user_id=int(val.discussion_author_id)).username, val.discussion_id)} for val in saved_threads_ids]
        chat_creation_url = '/new-conversation/{}/'.format(user_data.user_id)
        context = {
            'title': 'Profile',
            'logged_in': logged_in,
            'first_name': user_data_main.first_name,
            'last_name': user_data_main.last_name,
            'username': user_data.username,
            'email': user_data_main.email,
            'description': user_data.user_description,
            "followers": followers,
            'followers_count': len(followers),
            'following_users': following_users,
            'following_users_count': len(following_users),
            'profile_image': user_data.user_profile_image.url,
            'user_threads': user_threads,
            'user_threads_count': len(user_threads),
            'saved_threads': saved_threads,
            'saved_threads_count': len(saved_threads),
            'following': str(UserProfiles.objects.get(username=username).user_id) in UserProfiles.objects.get(user_id=user_id).user_following.split(","),
            'chat_creation_url': chat_creation_url,
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
                email_subject = 'popN - Profile Updated'
                email_body = 'Dear {},\n\nYour profile has been updated.\n\nThank You\n\nTeam popN'.format(user_data_main.first_name)
                email = EmailMessage(email_subject,email_body, to=[email_address])
                email.send()
                return redirect('/profile/')
        user_data = UserProfiles.objects.get(user_id=user_id)
        user_data_main = User.objects.get(username=user_data.username)
        form = EditProfileForm({
            'first_name': user_data_main.first_name,
            'last_name': user_data_main.last_name,
            'email': user_data_main.email,
            'description': user_data.user_description,
            'profile_image': user_data.user_profile_image,
            'logged_in': logged_in,
        })
        return render_template(request, 'community/editprofilepage.html', {"form":form})

def allconversationspages(request):
    logged_in, user_id = verify_request(request)
    if not logged_in:
        return redirect('/')
    else:
        context = {
            "title": "Conv",
            "conv_list": [],
            'logged_in': logged_in,
            "form": NewConversationGroupForm()
        }
        if request.method == "POST":
            form = NewConversationGroupForm(request.POST)
            if form.is_valid():
                usernames = list(set([username.strip() for username in form.cleaned_data.get('usernames').split(",")]))
                user_ids = [str(UserProfiles.objects.get(username=username).user_id) for username in usernames if username in [str(obj.username) for obj in UserProfiles.objects.all()]]
                if len(user_ids) > 0:
                    user_ids = ",".join(map(str,sorted(list(set([int(i) for i in user_ids+[user_id]])))))
                    conv = Conversations(user_ids=user_ids, admin_id=str(user_id))
                    conv.save()
                    return redirect("/conversations/{}/".format(conv.conversation_id))
                else:
                    return redirect("/conversations/")
        for conversation in Conversations.objects.all():
            if str(user_id) in conversation.user_ids.split(','):
                if conversation.conversation_title != '' and len(conversation.user_ids.split(',')) > 2:
                    name = conversation.conversation_title 
                else:
                    ref = conversation.user_ids.split(',')
                    ref.remove(str(user_id))
                    name = ", ".join(UserProfiles.objects.get(user_id=int(f_id)).username for f_id in ref if f_id != "")
                    if len(name) > 100:
                        name = name[:97] + "..."
                    if len(name) == 0:
                        Conversations.objects.get(conversation_id=conversation.conversation_id).delete()
                        continue
                context["conv_list"].append({"name":name, "url":"/conversations/{}".format(conversation.conversation_id)})
        return render_template(request, 'community/allconversationspage.html', context)

def selectconversationpage(request, conversation_id):
    logged_in, user_id = verify_request(request)
    if not logged_in or str(user_id) not in Conversations.objects.get(conversation_id=int(conversation_id)).user_ids.split(","):
        return redirect('/')
    else:
        conv = Conversations.objects.get(conversation_id=int(conversation_id))
        if request.method == "POST":
            form = ConversationForm(request.POST)
            if form.is_valid():
                comment = re.sub('[\xF0-\xF7][\x80-\xBF][\x80-\xBF][\x80-\xBF]', '', str(form.cleaned_data.get("message")))
                msg = ConversationMessages(user_id=int(user_id), conversation_id=int(conversation_id), message_text=comment)
                msg.save()
                conv.conversation_history = conv.conversation_history + "," + str(msg.message_id)
                conv.save()
        users = [int(val) for val in conv.user_ids.split(",") if val != '']
        raw_conv_data = conv.conversation_history.split(",")
        conv_data = []
        for message_id in raw_conv_data:
            if message_id != '':
                msg = ConversationMessages.objects.get(message_id=int(message_id))
                datestamp = msg.message_time
                message = msg.message_text
                username = UserProfiles.objects.get(user_id=int(msg.user_id)).username
                conv_data.append({"username":username, "datestamp":datestamp, "message":message})
        title = conv.conversation_title
        form = ConversationForm()
        current_date = datetime.datetime.now().date
        participants = []
        for user in conv.user_ids.split(","):
            data = {
                "username": UserProfiles.objects.get(user_id=int(user)).username + (" - admin" if int(conv.admin_id) == int(user) else ""),
                "profile_url": "/profile/view/{}/".format(int(user))
            }
            participants.append(data)
        if conv.conversation_title != '' and len(conv.user_ids.split(',')) > 2:
            name = conv.conversation_title 
        else:
            ref = conv.user_ids.split(',')
            ref.remove(str(user_id))
            name = ", ".join(UserProfiles.objects.get(user_id=int(f_id)).username for f_id in ref if f_id != "")
            if len(name) > 100:
                name = name[:97] + "..."
        context = {
            "form": form,
            "title": title,
            "conv_data": conv_data,
            'logged_in': logged_in,
            "conversation_id": conversation_id,
            "current_date": current_date,
            "participants": participants,
            "chat_title": name,
            }
        return render_template(request, 'community/conversationpage.html', context)

def newconversationpage(request, other_user_id):
    logged_in, user_id = verify_request(request)
    if not logged_in:
        return redirect('/')
    else:
        for conv in Conversations.objects.all():
            if str(user_id) in conv.user_ids.split(',') and str(other_user_id) in conv.user_ids.split(',') and len(conv.user_ids.split(',')) == 2:
                conv_id = conv.conversation_id
                break
        else:
            usrs = str(other_user_id) + "," + str(user_id)
            conv = Conversations(user_ids=usrs, admin_id=str(user_id))
            conv.save()
            conv_id = conv.conversation_id
        return redirect("/conversations/{}/".format(conv_id))

def selectdiscussionpage(request, username, discussion_id):
    logged_in, user_id = verify_request(request)
    if not logged_in:
        return redirect('/')
    else:
        discussion = CommunityDiscussions.objects.get(discussion_id=discussion_id)
        if request.method == "POST":
            save_switch = request.POST.get('switch', False)
            if save_switch:
                profile = UserProfiles.objects.get(user_id=int(user_id))
                saved_threads = profile.user_saved_threads.split(",")
                if str(discussion_id) in profile.user_saved_threads.split(","):
                    saved_threads.remove(str(discussion_id))
                    profile.user_saved_threads = ",".join(saved_threads)
                else:
                    profile.user_saved_threads = ",".join(saved_threads+[str(discussion_id)])
                profile.save()
            else:
                form = CommentForm(request.POST)
                if form.is_valid():
                    desc = form.cleaned_data.get('comment')
                    comment = CommunityComments(
                        discussion_id=discussion_id,
                        comment_author_id=user_id,
                        comment_description=re.sub('[\xF0-\xF7][\x80-\xBF][\x80-\xBF][\x80-\xBF]', '', str(desc))
                    )
                    if CommunityComments.objects.filter(discussion_id=discussion.discussion_id).count() < discussion.discussion_maximum_comments:
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
            "discussion_id": discussion_id,
            "saved": str(discussion_id) in UserProfiles.objects.get(user_id=int(user_id)).user_saved_threads.split(","),
            "tags": discussion.discussion_tags.split(","),
        }
        if context["editable"]:
            context["edit_url"] = "/edit-discussion/{}/{}/".format(username, discussion_id)
        for comment in CommunityComments.objects.filter(discussion_id=discussion_id):
            context["comments"].append({
                "author": UserProfiles.objects.get(user_id=comment.comment_author_id).username,
                "description": comment.comment_description,
                "pub_date": comment.comment_publish_date,
            })
        return render_template(request, "community/singlediscussionpage.html", context)

def editdiscussionpage(request, username, discussion_id):
    logged_in, user_id = verify_request(request)
    if not logged_in:
        return redirect('/')
    elif username != UserProfiles.objects.get(user_id=int(user_id)).username:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = DiscussionForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data.get('title')
                max_comments = form.cleaned_data.get('max_comments')
                description = form.cleaned_data.get('description')
                tags = ",".join(str(tag).strip().lower() for tag in form.cleaned_data.get('tags').split(","))
                discussion = CommunityDiscussions.objects.get(discussion_id=int(discussion_id))
                discussion.discussion_title=title
                discussion.discussion_description=re.sub('[\xF0-\xF7][\x80-\xBF][\x80-\xBF][\x80-\xBF]', '', str(description))
                discussion.discussion_maximum_comments=max_comments
                discussion.discussion_type="OPEN"
                discussion.discussion_author_id=str(user_id)
                discussion.discussion_tags = tags
                discussion.save()
                return redirect('/')
        discussion = CommunityDiscussions.objects.get(discussion_id=int(discussion_id))
        form_data = {
            "title": discussion.discussion_title,
            "description": discussion.discussion_description,
            "max_comments": discussion.discussion_maximum_comments,
            "tags": discussion.discussion_tags,
        }
        form = DiscussionForm(form_data)
        return render_template(request, 'community/newdiscussionpage.html', {"title":"Edit Discussion", "form":form, 'logged_in': logged_in})

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
                tags = ",".join(str(tag).strip().lower() for tag in form.cleaned_data.get('tags').split(","))
                discussion = CommunityDiscussions(
                    discussion_title=title,
                    discussion_description=re.sub('[\xF0-\xF7][\x80-\xBF][\x80-\xBF][\x80-\xBF]', '', str(description)),
                    discussion_maximum_comments=max_comments,
                    discussion_type="OPEN",
                    discussion_author_id=str(user_id),
                    discussion_tags=tags)
                discussion.save()
                return redirect('/')
        form = DiscussionForm()
        return render_template(request, 'community/newdiscussionpage.html', {"title":"New Discussion", "form":form, 'logged_in': logged_in})

def search(query, logged_in):
    threads = []
    users = []
    for thread in CommunityDiscussions.objects.all():
        for data in [thread.discussion_title, thread.discussion_description]:
            if query.lower() in data.lower():
                break
        else:
            continue
        threads.append({
            'card_title': thread.discussion_title,
            'card_text': thread.discussion_description,
        })
    for user in UserProfiles.objects.all():
        if query in user.username:
            users.append({
                'username': user.username,
                'url': "/profile/view/{}/".format(user.username),
            }) 
    res = {}
    if len(threads) > 0:
        res["threads"] = threads
    if len(users) > 0:
        res["users"] = users
    return res

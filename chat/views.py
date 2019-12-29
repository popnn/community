from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
import json

def verify_request(request):
    return request.COOKIES.get('id', None) is not None, request.COOKIES.get('id', None)

def index(request):
    logged_in, user_id = verify_request(request)
    if logged_in:
        return render(request, 'chat/index.html', {})
    else:
        return redirect("/")

def room(request, room_name):
    logged_in, user_id = verify_request(request)
    if logged_in:
        user_data = UserProfiles.objects.get(user_id=UserProfiles.objects.get(username=username).user_id)
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),
            'username': user_data.username,
            })
    else:
        return redirect("/")
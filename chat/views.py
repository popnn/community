from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json

def verify_request(request):
    return request.COOKIES.get('id', None) is not None, request.COOKIES.get('id', None)

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    logged_in, user_id = verify_request(request)
    if logged_in:
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name))
        })
    else:
        return redirect("/")
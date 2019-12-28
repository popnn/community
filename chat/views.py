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
from time import time as xTime
from pwa_webpush.utils import send_to_subscription


# Create your views here.
def verify_request(request):
    return request.COOKIES.get('id', None) is not None, request.COOKIES.get('id', None)

def render_template(request, template_name, context={}):
    response = render(request, template_name, context)
    response.set_cookie('load', datetime.datetime.now().strftime("%H:%M:%S.%f %b %d %Y"))
    return response

def homepage(request):
    return render_template(request, 'chat/homepage.html', {})

def chatroom(request, room_name):
    return render_template(request, 'chat/chatroom.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
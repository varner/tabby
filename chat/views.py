from django.shortcuts import render
from django.http import HttpResponse

from django_twilio.decorators import twilio_view
from twilio.twiml import Response

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# RECIEVE A NEW TEXT
@twilio_view
def sms(request):
    # PROCESS TEXT
    # if user exists:
    username = request.POST.get('From', '')
    if User.filter(username=username).exists():
        user = User.objects.get(username=username)
        if user.get_name():
            # it's ok to have a conversation
            pass
        else:
            onboard(user) 
    # GIVE EMPTY RESPONSE TO CALLBACK
    r = Response()
    return r

def onboard(User):
    mood = check_mood()
    ask_for_name()
    
    r = Response()
    return r
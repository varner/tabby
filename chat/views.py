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

    # GIVE EMPTY RESPONSE TO CALLBACK
    r = Response()
    return r
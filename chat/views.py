from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from twilio.twiml import Response
from chat.models import Caller, Message
# ----- experimental section ------
from . import processor
from .tasks import process_messages
from datetime import datetime


# Create your views here.
def index(request):
    return HttpResponse("GET OUT!")

@login_required
def enable_chaos(request):
    print datetime.now().time(), processor.during_freetime()
    process_messages()
    return HttpResponse("CHAOS....ENACTED...!!!")

@csrf_exempt
def sms(request):
    phone = request.POST.get('From', '')
    r = Response()
    if Caller.objects.filter(phone=phone).exists(): # DOES USER EXIST?
        caller = Caller.objects.get(phone=phone)
        if caller.isActive(): # AND IS NOT EXPIRED
            recieved_message = request.POST.get('Body', '')
            Message.objects.create_message(sender=caller, body=recieved_message)

    return HttpResponse(r.toxml(), content_type='text/xml')
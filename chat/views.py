from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
#from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from chat.models import Caller, Message

from twilio.rest import TwilioRestClient as Client
from datetime import datetime, date

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def check_phone(last_checked):
    collect_messages(last_checked)

    # FOR EVERY MESSAGE: read_message(message)
    #process_messages()
    #send_messages()

    # check schedule
    # schedule next phone check accordingly
    pass

def process_messages():
    pass

def read_message(message):
    caller = Caller.objects.get(phone=message.user)
    body  = message.body.lower()
    level = user.level

    if level is 0:
        ask_name(caller, message)
    elif level is 1:
        confirm_name(caller, message)
    elif level is 2:
        if "yes" in body:
            affirm_name(caller, message)
        elif "no" in body:
            ask_name(caller, message)
        else:
            clarify_name(caller, message)
    else:
        pass

def ask_name(caller, message):
    caller.level = 1
    caller.save()

    send_message(username, "uhh who r u")
    

def confirm_name(caller, message):
    name = message.body.lower().strip()

    caller.name = name
    caller.level = 2
    caller.save()

    send_message(username, "so ur name is %s?")

def clarify_name(caller, message):
    name = message.body.lower().strip()

    caller.name = name
    caller.level = 2
    caller.save()

    send_message(caller.phone, "uhhh so ur name is %s....yes or no??" % name)

def affirm_name(caller, message):
    response = caller.name + (caller.name[-1] * 4)
    send_message(user, response)
    send_message(user, "ok good to know")

    caller.level = 3
    caller.save()

def send_message(username, message):
    twilio_client.messages.create(
        to=username, 
        from_="", 
        body=message,
    )

def collect_messages(last_checked):
    accessed_users = set()

    for message in twilio_client.messages.list(date_sent=last_checked.date()):
        username = message.from_
        if (username in accessed_users or User.objects.filter(username=username).exists()):
            user = User.objects.get(username=username)
            
            if date_sent >= last_checked:
                if user.profile.isActive():
                    recieved_message = message.body
                    # IF MESSAGE ALREADY EXISTS
                    if Message.objects.filter(sender=user).exists():
                        # APPEND MESSAGE TO MESSAGE QUEUE
                        message = Message.objects.get(sender=user)
                        message.body += "\n%s" % recieved_message
                        message.last_updated = timezone.now()
                        message.save()
                    else: # ELSE MAKE MESSAGE
                        Message.objects.create_message(sender=user, body=recieved_message)
            else:
                break

# Create your views here.
def index(request):
    return HttpResponse("GET OUT!")

# RECIEVE A NEW TEXT
#@twilio_view
@csrf_exempt
def sms(request):
    username = request.POST.get('From', '')
    r = Response()
    if User.objects.filter(username=username).exists(): # DOES USER EXIST?
        user = User.objects.get(username=username)
        if user.profile.isActive(): # AND IS NOT EXPIRED
            recieved_message = request.POST.get('Body', '')
            # IF MESSAGE ALREADY EXISTS
            if Message.objects.filter(sender=user).exists():
                # APPEND MESSAGE TO MESSAGE QUEUE
                message = Message.objects.get(sender=user)
                message.body += "\n%s" % recieved_message
                message.last_updated = timezone.now()
                message.save()
            else: # ELSE MAKE MESSAGE
                Message.objects.create_message(sender=user, body=recieved_message)
                read_message(message)
                # THROW RESPONSE INTO QUEUE
            # GIVE EMPTY RESPONSE TO CALLBACK
            return HttpResponse(r.toxml(), content_type='text/xml')
    return HttpResponse(r.toxml(), content_type='text/xml')
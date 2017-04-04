from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
#from django_twilio.decorators import twilio_view
from twilio.twiml import Response


# Create your views here.
def index(request):
    return HttpResponse("GET OUT!")

# RECIEVE A NEW TEXT
#@twilio_view
def sms(request):
    # PROCESS TEXT
    # if user exists:
    username = request.POST.get('From', '')
    twiml = '<Response><Message>im still testing</Message></Response>'

    if User.objects.filter(username=username).exists(): # AND IS NOT EXPIRED
        recieved_message = request.POST.get('Body', '')
        user = User.objects.get(username=username)
        # IF MESSAGE ALREADY EXISTS
        if Message.filter(sender=user).exists():
            # APPEND MESSAGE TO MESSAGE QUEUE
            message = Message.objects.get(sender=user)
            message.body += "\n%s" % recieved_message
            message.last_updated = timezone.now()
            message.save()
        else: # ELSE MAKE MESSAGE
            Message.objects.create_message(sender=user, body=recieved_message)
            # THROW RESPONSE INTO QUEUE
        # GIVE EMPTY RESPONSE TO CALLBACK
        return HttpResponse(twiml, content_type='text/xml')
    # GIVE EMPTY RESPONSE TO CALLBACK
    return HttpResponse(twiml, content_type='text/xml')

'''def onboard(User):
    mood = check_mood()
    ask_for_name()

    r = Response()
    return r'''
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
#from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from chat.models import Caller, Message


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
                # THROW RESPONSE INTO QUEUE
            # GIVE EMPTY RESPONSE TO CALLBACK
            return HttpResponse(r.toxml(), content_type='text/xml')
    return HttpResponse(r.toxml(), content_type='text/xml')
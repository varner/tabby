from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
#from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from chat.models import Caller, Message


# Create your views here.
def index(request):
    return HttpResponse("GET OUT!")

#@login_required
#def collect(request):
#    processor.check_phone(timezone.now() - timezone.timedelta(hours=1))
#    return HttpResponse("I'M TRYING YO!")

# RECIEVE A NEW TEXT
#@twilio_view
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




#def collect_messages(last_checked):
#    accessed_callers = set()
#
#    for text in twilio_client.messages.list(date_sent=last_checked.date()):
#        logging.error("%s %s" % (text.date_created, text.body))
#        phone = text.from_
#        if (phone in accessed_callers or Caller.objects.filter(phone=phone).exists()):
#            caller = Caller.objects.get(phone=phone)
#            date_sent = text.date_sent.replace(tzinfo=pytz.utc)
#            logging.error(date_sent)
#            logging.error(text.body)
#            logging.error(last_checked)
#            if date_sent >= last_checked:
#                if caller.isActive():
#                    recieved_message = text.body
                    # IF MESSAGE ALREADY EXISTS
        #            if Message.objects.filter(sender=caller).exists():
        #                # APPEND MESSAGE TO MESSAGE QUEUE
        #                message = Message.objects.get(sender=caller)
        #                message.body += "\n%s" % recieved_message
        #                message.last_updated = timezone.now()
        #                message.save()
        #                logging.error("editing old message")
        #            else: # ELSE MAKE MESSAGE
        #                Message.objects.create_message(sender=caller, body=recieved_message)
        #                logging.error("making new message")
        #        else: logging.error("user not active???")
        #    else:
        #        logging.error("not within range")
        #        #break

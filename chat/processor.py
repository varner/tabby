from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from chat.models import Caller, Message
from twilio.rest import TwilioRestClient as Client
from datetime import datetime, date
import pytz

twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def check_phone():
    callers = dict()
    # read all the messages, compress into bundles
    messages = Message.objects.all().order_by('sent')
    for message in messages.iterator():
        if message.sender in callers.keys():
            callers[message.sender] += "\n" + message.body
        else:
            callers[message.sender] = message.body
        message.delete()
    # read and send message
    for key in callers.keys():
        print key, "KEYS"
        read_message(key, callers[key])
    # check schedule
    # schedule next phone check accordingly

def read_message(phone, message):
    caller = Caller.objects.get(phone=phone)
    body   = message.lower()
    lvl    = caller.level

    swear_word_list = "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/en"

    if lvl == 0:
        send_message(caller.phone, "wats ur name")
        caller.advanceLevel()
    elif lvl == 1:
        send_message(caller.phone, "hi %s" % body)
        caller.advanceLevel()
        caller.name = body
    elif lvl == 2:
        send_message(caller.phone, "you're level 2")
        caller.advanceLevel()
    else:
        print "help"
    caller.save()

def send_message(username, message):
    twilio_client.messages.create(
        to=username, 
        from_="+12164506309", 
        body=message,
    )

def during_freetime():
    #im_scared = [{ "start": datetime.time(7, 30, 0), \
    #  "end": datetime.time(10, 30, 0) \
    #}, { "start": datetime.time(13, 0, 0), \
    #  "end": datetime.time(17, 20, 0) \
    #}, { "start": datetime.time(19, 11, 0), \
    #  "end": datetime.time(19, 55, 0) \
    #}, { "start": datetime.time(20, 5, 0), \
    #  "end": datetime.time(23, 3, 20) \
    #}]
#
    #current = datetime.now().time()
    #for period in im_scared: 
    #    if current >= period['start'] and current < period['end']:
    #        return True
    return False
#def ask_name(caller, message):
#   caller.level = 1
#   caller.save()
#
#   send_message(username, "uhh who r u")
#       
#
#def confirm_name(caller, message):
#   name = message.body.lower().strip()
#
#   caller.name = name
#   caller.level = 2
#   caller.save()
#
#   send_message(username, "so ur name is %s?")
#
#def clarify_name(caller, message):
#   name = message.body.lower().strip()
#
#   caller.name = name
#   caller.level = 2
#   caller.save()
#
#   send_message(caller.phone, "uhhh so ur name is %s....yes or no??" % name)
#
#def affirm_name(caller, message):
#   response = caller.name + (caller.name[-1] * 4)
#   send_message(user, response)
#   send_message(user, "ok good to know")
#
#   caller.level = 3
#   caller.save()
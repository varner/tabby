from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from chat.models import Caller, Message
from twilio.rest import TwilioRestClient as Client
from datetime import datetime, date, time
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
    local = pytz.timezone ("America/New_York")
    schedule = [{"start": time(7,30), "end": time(10,30)}, 
    {"start": time(13), "end": time(17,20,22)}, 
    {"start": time(19,11), "end": time(19, 11)}]

    current = datetime.now().time()
    local_current = local.localize(current, is_dst=None)
    for period in schedule: 
        if local_current >= period['start'] and local_current < period['end']:
            return True
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
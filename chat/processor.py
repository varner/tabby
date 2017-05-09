from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from chat.models import Caller, Message
from twilio.rest import TwilioRestClient as Client
from datetime import datetime, date, time
import pytz
import urllib2
from random import randint

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
    mood   = during_freetime()
    caller = Caller.objects.get(phone=phone)
    body   = message.lower().strip()
    lvl    = caller.level

    if   lvl == 0:
        send_message(caller.phone, "hi%s uhhhh wats ur name lol" % ("!" * randint(0, 10)))
        caller.setLevel(1)
    elif lvl == 1:
        caller.setName(body) # set the name regardless because we can always rewrite if incorrect
        if is_rude(message):
            send_message(caller.phone, "uhm")
            end_message(caller.phone, "are u sure about that")
            caller.setLevel(2)
        else:
            send_message(caller.phone, "hi %s%s" % (body, "!" * randint(0, 5)))
            caller.setLevel(3)
    elif lvl == 2:
        # if was rude
        # yes
        if "y" in body:
            send_message(caller.phone, "ok whatever %s.......")
            caller.setLevel(3)
        else:
            # try again
            send_message(caller.phone, "thought so...cmon wats ur name")
            caller.setLevel(1)
    elif lvl == 3: 
        if mood is "freaky"\
        or mood is "cat_marnell"\
        or mood is "one_word"\
        or mood is "curt"\
        or mood is "punchy"\
        or mood is "on":          
            send_message(caller.phone, "too busy rn sorry%s" % ("!" * randint(0, 10)))
        #caller.advanceLevel()
    else:
        print "help"
    caller.save()
    
def send_message(username, message):
    twilio_client.messages.create(
        to=username, 
        from_="+12164506309", 
        body=message,
    )

# takes a string, returns True or False depending on whether a swear is in string
def is_rude(message):
    swear_list = "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/en"
    response = urllib2.urlopen(swear_list)
    html = response.read()
    swears = html.split('\n')

    rude = False
    for swear in swears:
        if swear in message:
            rude = True

def during_freetime():
    local = pytz.timezone("America/New_York")
    schedule = [
        {"start": time(0),     "end": time(3),      "mode": "freaky"     }, 
        {"start": time(3,1,17),"end": time(7,0,23), "mode": "cat_marnell"},
        {"start": time(9,30),  "end": time(12,00),  "mode": "one_word"   }, 
        {"start": time(12),    "end": time(15),     "mode": "curt"       }, 
        {"start": time(15),    "end": time(18),     "mode": "punchy"     }, 
        {"start": time(18),    "end": time(23, 59), "mode": "on"         }
    ]

    current = datetime.now()
    local_current = local.localize(current, is_dst=None).time()
    for period in schedule: 
        if local_current >= period['start'] and local_current < period['end']:
            print period['mode']
            return period['mode']
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
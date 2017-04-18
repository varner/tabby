from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

from chat.models import Caller, Message
from twilio.rest import TwilioRestClient as Client
from datetime import datetime, date
import pytz

twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def check_phone(last_checked):
    collect_messages(last_checked)

    # now get all the completed messages
    messages = Message.objects.all()
    for message in messages.iterator():
        # read and send message
        read_message(message)
        # then delete it from the archive
        message.delete()

    # check schedule
    # schedule next phone check accordingly

def read_message(message):
    caller = message.sender
    body   = message.body.lower()
    lvl    = caller.level

    swear_word_list = "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/en"

    if lvl == 0:
        send_message(caller.phone, "wats ur name")
    elif lvl == 1:
        pass
    elif lvl == 2:
        pass
    else:
        pass

def send_message(username, message):
    twilio_client.messages.create(
        to=username, 
        from_="+12164506309", 
        body=message,
    )

def collect_messages(last_checked):
    accessed_callers = set()

    for message in twilio_client.messages.list(date_sent=last_checked.date()):
        phone = message.from_
        if (phone in accessed_callers or Caller.objects.filter(phone=phone).exists()):
            caller = Caller.objects.get(phone=phone)
            date_sent = message.date_sent.replace(tzinfo=pytz.utc)
            if date_sent >= last_checked:
                if caller.isActive():
                    recieved_message = message.body
                    # IF MESSAGE ALREADY EXISTS
                    if Message.objects.filter(sender=caller).exists():
                        # APPEND MESSAGE TO MESSAGE QUEUE
                        message = Message.objects.get(sender=caller)
                        message.body += "\n%s" % recieved_message
                        message.last_updated = timezone.now()
                        message.save()
                    else: # ELSE MAKE MESSAGE
                        Message.objects.create_message(sender=caller, body=recieved_message)
            else:
                break

#   if level is 0:
#       ask_name(caller, message)
#   elif level is 1:
#       confirm_name(caller, message)
#   elif level is 2:
#       if "yes" in body:
#           affirm_name(caller, message)
#       elif "no" in body:
#           ask_name(caller, message)
#       else:
#           clarify_name(caller, message)
#   else:
#       pass

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
#

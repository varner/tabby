from django.utils import timezone
from django.contrib.auth.models import User

from chat.models import Profile, Message

from twilio.rest import TwilioRestClient as Client
from datetime import datetime, date

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
    user  = message.user
    level = user.level

    if level is 0:
        ask_name(user)
    elif level is 1:
        confirm_name(user)
    elif level is 2:
        #if yes:
        affirm_name(user)
        #else:
        confirm_name(user)
    else:
        pass

def ask_name(user):
    pass

def confirm_name(user):
    pass

def affirm_name(user):
    pass

def collect_messages(last_checked):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    accessed_users = set()

    for message in client.messages.list(date_sent=last_checked.date()):
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
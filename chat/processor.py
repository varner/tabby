from django.utils import timezone
from django.contrib.auth.models import User

from chat.models import Profile, Message

from twilio.rest import TwilioRestClient as Client
from datetime import datetime, date

def collect_messages(last_checked):
	client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
	
	checked_day   = last_checked.day
	checked_month = last_checked.month
	checked_year  = last_checked.year

	for message in client.messages.list(date_sent=date(checked_year, checked_month, checked_day)):
		username = message.from_
		if User.objects.filter(username=username).exists() and date_sent > last_checked: # and before expiration date!
    	    user = User.objects.get(username=username)
    	    if user.Profile.isActive():
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
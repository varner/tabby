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

	bodied = ""

	# A list of message objects with the properties described above
	for message in client.messages.list(date_sent=date(2017, 4, 11)):
	    if message.date_sent >= last_checked:
	    	user = message.from_
	    	bodied = message.body + "\n" + bodied
	    	#client.messages.delete(message.name)
	bodied = bodied.strip()
	last_checked = right_now
	print bodied

	for message in client.messages.list(date_sent=date(checked_year, checked_month, checked_day)):
		username = message.from_
		if User.objects.filter(username=username).exists(): # and last_checked
    	    print "user exists"
    	    recieved_message = message.body
    	    user = User.objects.get(username=username)
    	    # IF MESSAGE ALREADY EXISTS
    	    if Message.objects.filter(sender=user).exists():
    	        # APPEND MESSAGE TO MESSAGE QUEUE
    	        message = Message.objects.get(sender=user)
    	        message.body += "\n%s" % recieved_message
    	        message.last_updated = timezone.now()
    	        message.save()
    	    else: # ELSE MAKE MESSAGE
    	        Message.objects.create_message(sender=user, body=recieved_message)

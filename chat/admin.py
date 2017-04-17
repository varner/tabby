from django.contrib import admin
from chat.models import Caller, Message

# Register your models here.
admin.site.register(Caller)
admin.site.register(Message)
from django.contrib import admin
from chat.models import Caller, Message

# Define a new User admin
#class UserAdmin(BaseUserAdmin):
#    inlines = (ProfileInline, )

# Register your models here.
admin.site.register(Message)
admin.site.register(Caller)
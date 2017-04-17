from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from chat.models import Caller, Message

# Define a new User admin
#class UserAdmin(BaseUserAdmin):
#    inlines = (ProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(Message)
admin.site.register(Caller)
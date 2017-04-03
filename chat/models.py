from __future__ import unicode_literals
from django.db import models

import json
import urllib2

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

'''
PROFILE
'''
class Profile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(blank=True, default=0)
    trust = models.IntegerField(blank=True, default=30)
    subscription_end = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

'''
RECIEVED MESSAGES
'''
class Message(models.Model):
    sender       = models.ForeignKey(User, related_name="sender")
    last_updated = models.DateField(null=True, blank=True)
    content      = models.TextField(null=True, blank=True)
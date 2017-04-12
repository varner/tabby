from __future__ import unicode_literals
from django.db import models

import json
import urllib2
from datetime import date

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

'''
PROFILE
'''
class Profile(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(blank=True, default=0)
    trust = models.PositiveSmallIntegerField(blank=True, default=30)
    subscription_end = models.DateField(blank=True, default=date.today())

    def isActive(self):
        return (self.subscription_end >= date.today())

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


'''
MANAGE MESSAGES
'''
class MessageManager(models.Manager):
    def create_message(self, sender, body):
        message = self.create(sender=sender, body=body, last_updated=timezone.now)
        return message

'''
RECIEVED MESSAGES
'''
class Message(models.Model):
    sender       = models.ForeignKey(User, related_name="Sender")
    last_updated = models.DateField(default=timezone.now)
    body         = models.TextField(null=True, blank=True)

    objects = MessageManager()

    def __str__(self):
        return self.sender.username
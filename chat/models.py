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
class Caller(models.Model):
    phone = models.CharField(max_length=50)
    name  = models.CharField(max_length=50)
    # -----
    registered_on = models.DateField(default=date.today())
    subscription_end = models.DateField(blank=True, default=(date.today() + timedelta(days=30)))
    # -----
    level = models.PositiveSmallIntegerField(blank=True, default=0)
    trust = models.PositiveSmallIntegerField(blank=True, default=30)

    def isActive(self):
        return (self.subscription_end >= date.today())

    def advanceLevel(self):
        self.level += 1
        return level

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
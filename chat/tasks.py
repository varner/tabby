from __future__ import absolute_import, unicode_literals
from celery import shared_task
from . import processor

@shared_task
def process_messages():
	processor.check_phone()
	if processor.during_freetime():
		process_messages.apply_async(countdown=3600)
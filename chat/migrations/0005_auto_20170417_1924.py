# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-17 19:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20170417_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caller',
            name='registered_on',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='caller',
            name='subscription_end',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
    ]

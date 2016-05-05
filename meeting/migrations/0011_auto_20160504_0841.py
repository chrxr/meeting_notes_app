# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 08:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0010_remove_meeting_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Date'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='timeEnd',
            field=models.TimeField(blank=True, null=True, verbose_name='End time'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='timeStart',
            field=models.TimeField(blank=True, null=True, verbose_name='Start time'),
        ),
    ]
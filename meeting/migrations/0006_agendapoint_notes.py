# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0005_auto_20160418_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendapoint',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Notes'),
        ),
    ]

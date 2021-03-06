# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 20:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0014_auto_20160504_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
            ],
        ),
        migrations.RemoveField(
            model_name='agendapoint',
            name='notes',
        ),
        migrations.AddField(
            model_name='meetingnotes',
            name='agendaPoint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='meeting.AgendaPoint'),
        ),
        migrations.AddField(
            model_name='meetingnotes',
            name='meeting',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='meeting.Meeting'),
        ),
    ]

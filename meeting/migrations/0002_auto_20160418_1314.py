# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 13:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.TextField(verbose_name='Action')),
            ],
        ),
        migrations.CreateModel(
            name='AgendaPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Agenda point')),
                ('meeting', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='agenda_points', to='meeting.Meeting')),
            ],
        ),
        migrations.AddField(
            model_name='actions',
            name='meeting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='meeting.AgendaPoint'),
        ),
    ]

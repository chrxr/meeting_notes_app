from __future__ import unicode_literals

from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

# Create your models here.

class AgendaPoint(models.Model):
    meeting = ParentalKey('Meeting', related_name='agenda_points')
    title = models.CharField('Agenda point', max_length=255)
    description = models.TextField('Description', null=True, blank=True)
    timeStart = models.TimeField('Start time', null=True, blank=True)
    timeEnd = models.TimeField('End time', null=True, blank=True)
    notes = models.TextField('Notes', null=True, blank=True)

    def __str__(self):
        return self.title

class Action(models.Model):
    meeting = models.ForeignKey('AgendaPoint', related_name='actions')
    action = models.TextField('Action')

    def __str__(self):
        return self.action

class Meeting(ClusterableModel):
    title = models.CharField('Meeting title', max_length=255)
    dateTime = models.DateTimeField('Date & Time')

    def __str__(self):
        return self.title

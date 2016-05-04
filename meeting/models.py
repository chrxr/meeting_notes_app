from __future__ import unicode_literals

from django.db import models
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

# Create your models here.

class Person(models.Model):
    firstName = models.CharField('First name', max_length=40)
    secondName = models.CharField('Second name', max_length=40)
    email = models.EmailField('Email address', max_length=255)

    def __str__(self):
        return (self.firstName + ' ' + self.secondName)

class Attendee(models.Model):
    meeting = ParentalKey('Meeting', related_name='attendees')
    person = models.ForeignKey('Person', related_name='+')

    def __str__(self):
        return self.meeting.title +', ' + self.meeting.dateTime.strftime('%m/%d/%Y') + ': ' + self.person.firstName + ' ' + self.person.secondName

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
    assignee = models.ForeignKey('Person', related_name='+', blank=True, null=True)
    dueDate = models.DateTimeField('To be completed by', blank=True, null=True)

    def __str__(self):
        return self.action

class Meeting(ClusterableModel):
    title = models.CharField('Meeting title', max_length=255)
    date = models.DateField('Date', null=True, blank=True)
    timeStart = models.TimeField('Start time', null=True, blank=True)
    timeEnd = models.TimeField('End time', null=True, blank=True)
    location = models.CharField('Location', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title

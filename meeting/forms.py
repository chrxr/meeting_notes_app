from django import forms
from .models import Meeting, Attendee, Person
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'dateTime', 'location']

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        exclude = ['meeting'] 

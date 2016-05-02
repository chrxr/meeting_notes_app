from django import forms
from .models import Meeting, Attendee, Person, AgendaPoint
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

class AgendaForm(forms.ModelForm):
    class Meta:
        model = AgendaPoint
        fields = ['title', 'description', 'timeStart', 'timeEnd']
        widgets = {
            'timeStart': forms.TextInput(attrs={'placeholder': "HH:MM"}),
            'timeEnd': forms.TextInput(attrs={'placeholder': "HH:MM"}),
        }

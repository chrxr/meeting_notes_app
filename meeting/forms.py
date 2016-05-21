from django import forms
from .models import Meeting, Attendee, Person, AgendaPoint, Action, MeetingNotes
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

class NewMeetingForm(forms.Form):
    meeting_title = forms.CharField(label='Meeting title')
    date = forms.DateField(label="Date")
    start_time = forms.TimeField(label='Start time')
    end_time = forms.TimeField(label='End time')
    agenda_item = forms.ModelChoiceField(queryset=AgendaPoint.objects.all())


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'date', 'timeStart', 'timeEnd', 'location']
        widgets = {
            'timeStart': forms.TextInput(attrs={'placeholder': "HH:MM"}),
            'timeEnd': forms.TextInput(attrs={'placeholder': "HH:MM"}),
        }

class AttendeeForm(forms.ModelForm):
    class Meta:
        model = Attendee
        exclude = ['meeting']

class AddAgendaForm(forms.ModelForm):
    class Meta:
        model = AgendaPoint
        fields = ['title', 'duration',]

class AgendaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs.pop('state'):
            self.state = kwargs.pop('state')
        if self.state == 'edit':
            super(AgendaForm,self).__init__(*args,**kwargs)
    class Meta:
        model = AgendaPoint
        fields = ['title', 'description', 'duration',]

class ActionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.meeting_id = kwargs.pop('meeting_id')
        super(ActionForm,self).__init__(*args,**kwargs)
        agendaPoints = AgendaPoint.objects.filter(meeting = self.meeting_id).values_list('id','title')
        # assignee = Attendee.objects.filter(meeting = self.meeting_id).values_list('id','person__firstName')
        self.fields['agendaPoint'].choices = agendaPoints
        # self.fields['assignee'].choices = assignee

    class Meta:
        model = Action
        fields = ['agendaPoint', 'action', 'assignee', 'dueDate']

class MeetingNotesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.meeting_id = kwargs.pop('meeting_id')
        super(MeetingNotesForm,self).__init__(*args,**kwargs)
        agendaPoints = AgendaPoint.objects.filter(meeting = self.meeting_id).values_list('id','title')
        print agendaPoints
        self.fields['agendaPoint'].choices = agendaPoints

    class Meta:
        model = MeetingNotes
        fields = ['agendaPoint', 'notes']

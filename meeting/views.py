from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .forms import MeetingForm, AttendeeForm, AgendaForm
from .models import Meeting, Attendee, AgendaPoint
from django.forms import formset_factory
import datetime


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def createMeeting(request, meeting_id=None):
    if request.method == 'POST':
        if meeting_id:
            meeting = Meeting.objects.get(pk=meeting_id)
            mform = MeetingForm(request.POST, instance=meeting)
        else:
            mform = MeetingForm(request.POST, instance=Meeting())
        if mform.is_valid():
            new_meeting = mform.save()
            return HttpResponseRedirect(reverse('manage-meeting', args=[new_meeting.pk]))
    elif meeting_id:
        meeting = Meeting.objects.get(pk=meeting_id)
        form = MeetingForm(instance=meeting)
    else:
        form = MeetingForm(instance=Meeting())
    return render(request, 'meeting/create-meeting-form.html', {'form': form, 'meeting_id': meeting_id})

def addAttendees(request, meeting_id):
    AttendeeFormSet = formset_factory(AttendeeForm, extra=2)
    aforms = AttendeeFormSet(request.POST or None)
    for af in aforms:
        print af
    if request.method == 'POST':
        meeting = Meeting.objects.get(pk=meeting_id)
        if all([af.is_valid() for af in aforms]):
            for af in aforms:
                new_attendee = af.save(commit=False)
                new_attendee.meeting = meeting
                new_attendee.save()
            return HttpResponseRedirect(reverse('add-agenda', args=[meeting.pk]))
    else:
        return render(request, 'meeting/add-attendee-form.html', {'form': aforms})

def addAgendaPoints(request, meeting_id):
    AgendaFormSet = formset_factory(AgendaForm)
    aforms = AgendaFormSet(request.POST or None)
    if request.method == 'POST':
        meeting = Meeting.objects.get(pk=meeting_id)
        if all([af.is_valid() for af in aforms]):
            for af in aforms:
                new_agenda_point = af.save(commit=False)
                new_agenda_point.meeting = meeting
                new_agenda_point.save()
            return HttpResponse("YAY!")
    else:
        return render(request, 'meeting/add-agenda-form.html', {'form': aforms})

def viewMeetings(request):
    meetings = Meeting.objects.filter(dateTime__gt=datetime.date.today())
    return render(request, 'meeting/view-meetings.html', {'meetings': meetings})

def manageMeeting(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    return render(request, 'meeting/manage-meeting.html', {'meeting': meeting})

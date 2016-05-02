from django import forms
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .forms import MeetingForm, AttendeeForm, AgendaForm
from .models import Meeting, Attendee, AgendaPoint
from django.forms import formset_factory, inlineformset_factory
import datetime


#### General to do
# - Clean up display of templates
# - Add in field types for times and dates
# - View agenda points
# - Add in more detailed form validation

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


##### Stuff to do for attendees
# - People can only be added once
# - You can add a new person inline

def editAttendees(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    AttendeeFormSet = inlineformset_factory(Meeting, Attendee, fields=('person',), extra=0)
    if request.method == 'POST':
        aforms = AttendeeFormSet(request.POST, prefix='attendees', instance=meeting)
        if aforms.is_valid():
            aforms.save()
            return HttpResponseRedirect(reverse('manage-meeting', args=[meeting_id]))
        else:
            return HttpResponse(aforms.errors)
    else:
        aforms = AttendeeFormSet(instance=meeting)
        return render(request, 'meeting/add-attendee-form.html', {'form': aforms, 'meeting_id': meeting_id})

def addAttendees(request, meeting_id):
    existingAttendees = Attendee.objects.filter(meeting=meeting_id)
    AttendeeFormSet = formset_factory(AttendeeForm)
    aforms = AttendeeFormSet(request.POST or None)
    if request.method == 'POST':
        meeting = Meeting.objects.get(pk=meeting_id)
        if all([af.is_valid() for af in aforms]):
            for af in aforms:
                new_attendee = af.save(commit=False)
                new_attendee.meeting = meeting
                new_attendee.save()
            return HttpResponseRedirect(reverse('manage-meeting', args=[meeting_id]))
    elif existingAttendees:
        return HttpResponseRedirect(reverse('edit-attendees', args=[meeting_id]))
    else:
        return render(request, 'meeting/add-attendee-form.html', {'form': aforms})

def editAgendaPoints(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    AgendaFormSet = inlineformset_factory(Meeting, AgendaPoint, exclude=('meeting','notes'), extra=0)
    if request.method == 'POST':
        aforms = AgendaFormSet(request.POST, prefix='agenda_points', instance=meeting)
        if aforms.is_valid():
            aforms.save()
            return HttpResponseRedirect(reverse('manage-meeting', args=[meeting_id]))
        else:
            return HttpResponse(aforms.errors)
    else:
        aforms = AgendaFormSet(instance=meeting)
        return render(request, 'meeting/add-agenda-form.html', {'form': aforms})


def addAgendaPoints(request, meeting_id):
    existingAgenda = AgendaPoint.objects.filter(meeting=meeting_id)
    AgendaFormSet = formset_factory(AgendaForm)
    aforms = AgendaFormSet(request.POST or None)
    if request.method == 'POST':
        meeting = Meeting.objects.get(pk=meeting_id)
        if all([af.is_valid() for af in aforms]):
            for af in aforms:
                new_agenda_point = af.save(commit=False)
                new_agenda_point.meeting = meeting
                new_agenda_point.save()
            return HttpResponseRedirect(reverse('manage-meeting', args=[meeting_id]))
    elif existingAgenda:
        return HttpResponseRedirect(reverse('edit-agenda', args=[meeting_id]))
    else:
        return render(request, 'meeting/add-agenda-form.html', {'form': aforms})

def viewMeetings(request):
    meetings = Meeting.objects.filter(dateTime__gt=datetime.date.today())
    return render(request, 'meeting/view-meetings.html', {'meetings': meetings})

def meetingDetails(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    attendees = Attendee.objects.filter(meeting=meeting_id)
    agenda_points = AgendaPoint.objects.filter(meeting=meeting_id)
    return render(request, 'meeting/meeting-details.html', {'meeting': meeting, 'attendees': attendees, 'agenda_points': agenda_points})

def manageMeeting(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    return render(request, 'meeting/manage-meeting.html', {'meeting': meeting})

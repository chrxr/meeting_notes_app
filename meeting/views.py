from django import forms
from django.core import serializers
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .forms import MeetingForm, AttendeeForm, AgendaForm, MeetingNotesForm, ActionForm, AddAgendaForm, AttendeeForm, NewAttendeeForm
from .models import Meeting, Attendee, AgendaPoint, Person, MeetingNotes, Action
from django.forms import formset_factory, inlineformset_factory, BaseFormSet
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
        else:
            messages.error(request, "Error")
    elif meeting_id:
        meeting = Meeting.objects.get(pk=meeting_id)
        mform = MeetingForm(instance=meeting)
    else:
        mform = MeetingForm(instance=Meeting())
    return render(request, 'meeting/create-meeting-form.html', {'form': mform, 'meeting_id': meeting_id})



def newCreateMeeting(request, meeting_id=None):
    mform = MeetingForm(request.POST or None)
    agendaFormSet = formset_factory(AddAgendaForm, min_num=0, formset=RequiredFormSet)
    aforms = agendaFormSet(request.POST or None, prefix='agenda_points',)
    attendeeFormSet = formset_factory(NewAttendeeForm)
    atforms = attendeeFormSet(request.POST or None, prefix='attendees')

    if request.method == 'POST':
        if mform.is_valid():
            new_meeting = mform.save()
        else:
            return HttpResponse(mform.errors)
        if all([af.is_valid() for af in aforms]):
            for af in aforms:
                new_agenda_point = af.save(commit=False)
                new_agenda_point.meeting = new_meeting
                new_agenda_point.save()
        else:
            return HttpResponse(aforms.errors)
        if all([atf.is_valid() for atf in atforms]):
            for atf in atforms:
                new_attendee = atf.save(commit=False)
                new_attendee.meeting = new_meeting
                new_attendee.save()
        else:
            return HttpResponse(atforms.errors)
        return HttpResponseRedirect(reverse('manage-meeting', args=[new_meeting.pk]))
    else:
        return render(request, 'meeting/new-create-meeting-form.html', {'mform': mform,'aforms': aforms, 'atforms': atforms, 'meeting_id': meeting_id})





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
                try:
                    new_attendee.meeting = meeting
                    new_attendee.save()
                except:
                    messages.error(request, "Error")

            return HttpResponseRedirect(reverse('manage-meeting', args=[meeting_id]))
        else:
            return HttpResponse(aforms.errors)
    elif existingAttendees:
        return HttpResponseRedirect(reverse('edit-attendees', args=[meeting_id]))
    else:
        return render(request, 'meeting/add-attendee-form.html', {'form': aforms})

def editAgendaPoints(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    AgendaFormSet = inlineformset_factory(Meeting, AgendaPoint, exclude=('meeting','notes'), extra=0)
    current_agenda_items = AgendaPoint.objects.filter(meeting=meeting_id)
    total_agenda_length = sum([d.duration for d in current_agenda_items])
    if meeting.timeStart:
        meeting_length = calculate_meeting_length(meeting)
    else:
        meeting_length = None
    if request.method == 'POST':
        aforms = AgendaFormSet(request.POST, prefix='agenda_points', instance=meeting)
        if aforms.is_valid():
            aforms.save()
            return HttpResponseRedirect(reverse('manage-meeting', args=[meeting_id]))
        else:
            return HttpResponse(aforms.errors)

    else:
        aforms = AgendaFormSet(instance=meeting)
        return render(request, 'meeting/add-agenda-form.html', {'form': aforms, 'meeting_length': meeting_length})


def addAgendaPoints(request, meeting_id):
    existingAgenda = AgendaPoint.objects.filter(meeting=meeting_id)
    meeting = Meeting.objects.get(pk=meeting_id)
    AgendaFormSet = formset_factory(AgendaForm)
    aforms = AgendaFormSet(request.POST or None)
    meeting_length = calculate_meeting_length(meeting)
    if request.method == 'POST':
        if all([af.is_valid() for af in aforms]):
            for af in aforms:
                new_agenda_point = af.save(commit=False)
                new_agenda_point.meeting = meeting
                new_agenda_point.save()
            return HttpResponseRedirect(reverse('manage-meeting', args=[meeting_id]))
    elif existingAgenda:
        return HttpResponseRedirect(reverse('edit-agenda', args=[meeting_id]))
    else:
        return render(request, 'meeting/add-agenda-form.html', {'form': aforms, 'meeting_length': meeting_length})

def viewMeetings(request):
    meetings = Meeting.objects.filter(date__gt=datetime.date.today())
    return render(request, 'meeting/view-meetings.html', {'meetings': meetings})

def meetingDetails(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    attendees = Attendee.objects.filter(meeting=meeting_id)
    agenda_points = AgendaPoint.objects.filter(meeting=meeting_id)
    return render(request, 'meeting/meeting-details.html', {'meeting': meeting, 'attendees': attendees, 'agenda_points': agenda_points})

def manageMeeting(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    return render(request, 'meeting/manage-meeting.html', {'meeting': meeting})

def meetingNotes(request, meeting_id):
    meeting = Meeting.objects.get(pk=meeting_id)
    attendees = Attendee.objects.filter(meeting=meeting_id)
    agenda_points = AgendaPoint.objects.filter(meeting=meeting_id)
    NotesFormSet = formset_factory(MeetingNotesForm)
    ActionFormSet = formset_factory(ActionForm)
    nforms = NotesFormSet(request.POST or None, prefix='notes', form_kwargs={'meeting_id': meeting_id})
    aforms = ActionFormSet(request.POST or None, prefix='actions', form_kwargs={'meeting_id': meeting_id})
    if request.method == 'POST':
        if all([af.is_valid() for af in aforms]):
            for af in aforms:
                new_action = af.save(commit=False)
                new_action.meeting = meeting
                new_action.save()
        else:
            return HttpResponse(aforms.errors)
        if all([nf.is_valid() for nf in nforms]):
            for nf in nforms:
                new_note = nf.save(commit=False)
                new_note.meeting = meeting
                new_note.save()
        else:
            return HttpResponse(aforms.errors)
        return HttpResponseRedirect(reverse('manage-meeting', args=[meeting_id]))
    else:
        return render(request, 'meeting/meeting-notes.html', {'meeting': meeting, 'agenda_points': agenda_points, 'attendees': attendees, 'nforms': nforms, 'aforms': aforms})

def returnNames(request):
    people = Person.objects.all()
    data = serializers.serialize('json', people)
    return HttpResponse(data)


#### HELPERS

def calculate_meeting_length(meeting):
    start = datetime.datetime.combine(meeting.date, meeting.timeStart)
    end = datetime.datetime.combine(meeting.date, meeting.timeEnd)
    meeting_length_td = end - start
    meeting_length_mins = meeting_length_td.total_seconds() / 60
    return meeting_length_mins


class RequiredFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

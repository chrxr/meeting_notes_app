from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from .forms import MeetingForm, AttendeeForm
from .models import Meeting, Attendee


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def createMeeting(request):
    if request.method == 'POST':

        mform = MeetingForm(request.POST, instance=Meeting())
        # aforms = [AttendeeForm(request.POST, prefix=str(x), instance=Attendee()) for x in range(0,3)]
        # if mform.is_valid() and all([af.is_valid() for af in aforms]):
        #     new_meeting = mform.save()
        #     for af in aforms:
        #         new_attendee = af.save(commit=False)
        #         new_attendee.meeting = new_meeting
        #         new_attendee.save()
        if mform.is_valid():
            new_meeting = mform.save()

            return HttpResponse("YAY!")
    else:
        form = MeetingForm(instance=Meeting())
        # aforms = [AttendeeForm(prefix=str(x), instance=Attendee()) for x in range (0,3)]

    # return render(request, 'meeting/meeting-form.html', {'meeting_form': mform, 'attendee_forms': aforms})

    return render(request, 'meeting/form.html', {'form': form})

def addAttendees(request, meeting_id):
    if request.method == 'POST':
        aforms = [AttendeeForm(request.POST, prefix=str(x), instance=Attendee()) for x in range(0,3)]
        meeting = Meeting.objects.get(pk=meeting_id)
        if all([af.is_valid() for af in aforms]):
            for af in aforms:
                new_attendee = af.save(commit=False)
                new_attendee.meeting = meeting
                new_attendee.save()
            return HttpResponse("YAY!")
    else:
        aforms = [AttendeeForm(prefix=str(x), instance=Attendee()) for x in range (0,3)]

    return render(request, 'meeting/form.html', {'form': aforms})

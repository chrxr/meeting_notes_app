from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from .forms import MeetingForm, AttendeeForm
from .models import Meeting, Attendee


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def createMeeting(request):
    if request.method == 'POST':
        pass
        # form = StoryForm(request.POST)
        # if form.is_valid():
        #     new_story = form.save(commit=False)
        #     story_slug = slugify(new_story.title)
        #     slug_check = story.objects.filter(slug=story_slug)
        #     if slug_check:
        #         return HttpResponse('Oh! Sorry, that slug already exists.')
        #     else:
        #         print('This is about to be saved')
        #         new_story.save()
        #         return HttpResponse("Thanks!")
    else:
        mform = MeetingForm(instance=Meeting())
        aforms = [AttendeeForm(prefix=str(x), instance=Attendee()) for x in range (0,3)]

    return render_to_response('meeting/meeting-form.html', {'meeting_form': mform, 'attendee_forms': aforms})

    # return render(request, 'meeting/meeting-form.html', {'form': form})

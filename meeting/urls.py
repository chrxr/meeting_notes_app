from django.conf.urls import url, include
from django.views.generic.base import RedirectView, TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='meeting/home.html'), name='home'),
    url(r'^meetings/$', views.viewMeetings, name='view-meetings'),
    url(r'^meetings/create-meeting/$', views.createMeeting, name='create-meeting'),
    url(r'^meetings/([0-9]+)/add-attendees/$', views.addAttendees, name='add-attendees'),
    url(r'^meetings/([0-9]+)/edit-attendees/$', views.editAttendees, name='edit-attendees'),
    url(r'^meetings/([0-9]+)/edit-agenda/$', views.editAgendaPoints, name='edit-agenda'),
    url(r'^meetings/([0-9]+)/add-agenda/$', views.addAgendaPoints, name='add-agenda'),
    url(r'^meetings/([0-9]+)/$', RedirectView.as_view(pattern_name='manage-meeting', permanent=False), name='manage-redirect'),
    url(r'^meetings/([0-9]+)/manage/$', views.manageMeeting, name='manage-meeting'),
    url(r'^meetings/([0-9]+)/meeting-details/$', views.meetingDetails, name='meeting-details'),
    url(r'^meetings/([0-9]+)/edit/$', views.createMeeting, name='edit-meeting'),
]

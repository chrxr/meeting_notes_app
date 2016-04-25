from django.conf.urls import url, include
from django.views.generic.base import RedirectView, TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='meeting/home.html'), name='home'),
    url(r'^meetings/$', views.viewMeetings, name='view-meetings'),
    url(r'^meetings/create-meeting/$', views.createMeeting, name='create-meeting'),
    url(r'^meetings/([0-9]+)/add-attendees/$', views.addAttendees, name='add-attendees'),
    url(r'^meetings/([0-9]+)/add-agenda/$', views.addAgendaPoints, name='add-agenda'),
    url(r'^meetings/([0-9]+)/manage/$', views.manageMeeting, name='manage-meeting'),
    url(r'^meetings/([0-9]+)/edit/$', views.createMeeting, name='edit-meeting'),
]

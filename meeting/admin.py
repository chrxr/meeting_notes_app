from django.contrib import admin
from .models import Meeting, Action, AgendaPoint, Attendee, Person, Action

class AttendeeInline(admin.StackedInline):
    model = Attendee
    extra = 1

class AgendaPointInline(admin.StackedInline):
    model = AgendaPoint
    extra = 1

class ActionInline(admin.StackedInline):
    model = Action
    extra = 1

class MeetingAdmin(admin.ModelAdmin):
    inlines = [AgendaPointInline, AttendeeInline]

class AgendaPointAdmin(admin.ModelAdmin):
    inlines = [ActionInline]

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Action)
admin.site.register(Person)
admin.site.register(Attendee)
admin.site.register(AgendaPoint, AgendaPointAdmin)

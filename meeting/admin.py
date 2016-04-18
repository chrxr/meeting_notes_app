from django.contrib import admin
from .models import Meeting, Action, AgendaPoint

class AgendaPointInline(admin.StackedInline):
    model = AgendaPoint
    extra = 1

class ActionInline(admin.StackedInline):
    model = Action
    extra = 3

class MeetingAdmin(admin.ModelAdmin):
    inlines = [AgendaPointInline]

class AgendaPointAdmin(admin.ModelAdmin):
    inlines = [ActionInline]

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Action)
admin.site.register(AgendaPoint, AgendaPointAdmin)

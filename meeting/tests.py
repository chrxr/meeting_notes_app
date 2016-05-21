from django.test import TestCase, Client
from .models import Person, Meeting, AgendaPoint, Action
# Create your tests here.

c = Client()

class MeetingTestCase(TestCase):
    def setUp(self):
        Meeting.objects.create(
            title = "meeting",
            date = "2012-12-12",
            timeStart = "12:12",
            timeEnd = "13:13",
            location = "Birmingham",
        )

    def test_meeting_name(self):
        meeting = Meeting.objects.get(title = "meeting")
        self.assertEqual(meeting.__str__(), "meeting")

class PersonTestCase(TestCase):
    def setUp(self):
        Person.objects.create(
            firstName = "A",
            secondName = "Person",
            email = "blurgh@example.com"
        )

    def test_person_name(self):
        person = Person.objects.get(firstName = "A")
        self.assertEqual(person.__str__(), "A Person")


class AgendaPointTestCase(TestCase):
    def setUp(self):
        meeting = Meeting.objects.create(title="Meeting")
        # meeting = Meeting.objects.get(title="Meeting")
        AgendaPoint.objects.create(
            title = "Agenda point",
            meeting = meeting,
            description = "A description",
            duration = "50"
        )

    def test_agenda_name(self):
        agenda_point = AgendaPoint.objects.get(title = "Agenda point")
        self.assertEqual(agenda_point.__str__(), "Agenda point")

    def test_agenda_no_title(self):
        meeting = Meeting.objects.create(title="Meeting")
        agenda = AgendaPoint.objects.create(
            meeting = meeting,
            description = "A description",
            duration = "50"
        )
        test_url = '/meetings/' + str(agenda.pk) + '/edit-agenda/'
        response = c.get(test_url)
        self.assertEqual(response.status_code, 500)


class ActionTestCase(TestCase):
    def setUp(self):
        meeting = Meeting.objects.create(title="Meeting")
        agenda_point = AgendaPoint.objects.create(
                            title = "Agenda point",
                            meeting = meeting,
                        )
        person = Person.objects.create(firstName = "A", secondName = "Person", email = "blurgh@example.com")
        Action.objects.create(
            action = "Action",
            agendaPoint = agenda_point,
            meeting = meeting,
            assignee = person,
            dueDate = "2012-12-12"
        )

    def test_action_name(self):
        action = Action.objects.get(action = "Action")
        self.assertEqual(action.__str__(), "Action")

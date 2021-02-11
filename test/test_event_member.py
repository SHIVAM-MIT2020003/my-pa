from django.test import TestCase
from mypa.audio_recorder.models import Member
from mypa.audio_recorder.models import Event

class MemberTestCase(TestCase):
    def setUp(self):
        global event1
        global event2
        global event3
        event1 = Event.objects.create(id="1", start_date="04-04-2018", end_date="05-04-2018",organiser = "hashedin", creator = "Shivam", title="smasya ka samadhan", start_time="8:30AM")
        event2 = Event.objects.create(id="2", start_date="08-04-2018", end_date="08-04-2018", organiser="hashedin", creator="Akshat", title="kal ki fight ka solution", start_time="1:30AM")
        event3 = Event.objects.create(id="3", start_date="04-04-2018", end_date="05-05-2018", organiser="hashedin", creator="shivam", title="Welcome those jinko hashedin se bhagana hai", start_time="12:01AM")

        Member.objects.create(user_name="Shivam", email_id = "shivam.gupta@hashedin.com", attendees=event1)
        Member.objects.create(user_name="Rahul", email_id= "rahul.sigh@hashedin.com", attendees=event1)
        Member.objects.create(user_name="Ravi", email_id="ravi.hegde@hashedin.com",attendees=event1)

        Member.objects.create(user_name="Akshat", email_id="akshat.mathur@hashedin.com", attendees=event2)
        Member.objects.create(user_name="John", email_id="john.hegde@hashedin.com", attendees=event2)
        Member.objects.create(user_name="Shaun", email_id="shaun.michel@gmail.com", attendees=event2)

        Member.objects.create(user_name="Phenom", email_id="phenom.jhon@gmail.com", attendees=event3)
        Member.objects.create(user_name="Michel", email_id="michel.hussy@gmail.com", attendees=event3)

    def test_members(self):

        shivam = Member.objects.get(user_name="Shivam")
        rahul = Member.objects.get(user_name="Rahul")
        ravi = Member.objects.get(user_name="Ravi")
        akshat = Member.objects.get(user_name="Akshat")
        john = Member.objects.get(user_name="John")
        shaun = Member.objects.get(user_name="Shaun")
        phenom = Member.objects.get(user_name="Phenom")
        michel = Member.objects.get(user_name="Michel")

        self.assertEqual(event1.id, "1")
        self.assertEqual(event2.id, "2")
        self.assertEqual(event3.id, "3")
        self.assertEqual(shivam.details(), 'Shivam shivam.gupta@hashedin.com 1')
        self.assertEqual(rahul.details(), 'Rahul rahul.sigh@hashedin.com 1')
        self.assertEqual(ravi.details(), 'Ravi ravi.hegde@hashedin.com 1')
        self.assertEqual(akshat.details(), 'Akshat akshat.mathur@hashedin.com 2')
        self.assertEqual(john.details(), 'John john.hegde@hashedin.com 2')
        self.assertEqual(shaun.details(), 'Shaun shaun.michel@gmail.com 2')
        self.assertEqual(phenom.details(), 'Phenom phenom.jhon@gmail.com 3')
        self.assertEqual(michel.details(), 'Michel michel.hussy@gmail.com 3')





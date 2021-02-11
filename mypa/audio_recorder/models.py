from django.db import models

class AudioFiles(models.Model):
    id = models.AutoField(primary_key=True)
    audio = models.FileField(upload_to = 'media/')

class Event(models.Model):
    class Meta:
        db_table = "event"

    id = models.CharField(max_length=100, null=False, primary_key=True)
    start_date = models.CharField(max_length=100, null=False)
    end_date = models.CharField(max_length=20)
    organiser = models.CharField(max_length=50)
    creator = models.CharField(max_length=50)
    title = models.CharField(max_length=50,null=False,default="No Title")
    start_time = models.CharField(max_length=15,null=False,default="No Time Set")
class Member(models.Model):
    class Meta:
        db_table = "member"

    user_name = models.CharField(max_length=100, null = False)
    email_id = models.CharField(max_length=100)
    attendees = models.ForeignKey(Event, db_index=True, on_delete=models.CASCADE)

    def details(self):
        return self.user_name + " " + self.email_id + " " + self.attendees.id



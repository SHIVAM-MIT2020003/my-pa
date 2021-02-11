from django.core.management.base import BaseCommand
from ....audio_recorder import views
class Command(BaseCommand):
    def handle(self, *args, **options):
        views.call_twilio()

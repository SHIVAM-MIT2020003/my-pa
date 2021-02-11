from django.core.management.base import BaseCommand
import nltk


class Command(BaseCommand):
    def handle(self, *args, **options):
        nltk.download('all')

from django.core.management.base import BaseCommand
from metanews.apps.collector.models import Author, Copy


class Command(BaseCommand):

    def handle(self, *args, **options):
        for au in Author.objects.all():
            sex = au.get_sex()
            urls = map(lambda x: x.url, au.copy.all())
            print "%s %s %s" % (au.name, sex, au.copy.all().count())
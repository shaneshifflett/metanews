from django.core.management.base import BaseCommand
from metanews.apps.collector.models import Author


class Command(BaseCommand):

    def handle(self, *args, **options):
        for au in Author.objects.all():
            sex = au.get_sex()
            urls = map(lambda x: x.url, au.articles.all())
            print "%s %s %s %s" % (au.name, sex, au.articles.all().count(), au.sex_confidence)
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from metanews.apps.collector.models import Author, Article, Organization
from BeautifulSoup import BeautifulSoup
import itertools
import requests
from django.conf import settings

org, created = Organization.objects.get_or_create(name="The New York Times")

class Command(BaseCommand):

    def handle(self, *args, **options):
        print "Authors=%s" % Author.objects.filter(organization=org).count()
        import pdb;pdb.set_trace()
        Author.objects.filter(organization=org).delete()
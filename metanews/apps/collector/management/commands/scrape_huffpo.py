from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from metanews.apps.collector.models import Author, Article, Organization
from datetime import datetime
from BeautifulSoup import BeautifulSoup
import itertools
import requests
from django.conf import settings

print settings.SITE_ROOT

org, created = Organization.objects.get_or_create(name="The Huffington Post")

def create_copy(author, url, content, place):
    copy, created = Article.objects.get_or_create(url=url)
    copy.text = content
    copy.featured_at = place
    copy.save()
    author.articles.add(copy)

def clean_link(url):
    url = url.split("#")[0]
    url = url.split("?")[0]
    return url

def do_work(links, place):
    for link in links:
        url = clean_link(link['href'])
        if len(url.split("http://")) > 1:
            fn = slugify(url)
            print "getting url = %s @ %s" % (url, datetime.now())
            try:
                with open(settings.SITE_ROOT+"/data/scrapes/huffpo/"+fn, "rb") as f:
                    content = f.read()
            except IOError:
                page = requests.get(url)
                with open(settings.SITE_ROOT+"/data/scrapes/huffpo/"+fn, "wb") as f:
                    f.write(page.content)
                    content = page.content
            pagesoup = BeautifulSoup(content)
            spans = pagesoup.findAll("span", "color_1A1A1A")
            if len(spans) == 1:
                name = spans[0].text.split("By ")[1]
                if len(name.split(' and ')) > 1:
                    for nm in name.split(' and '):
                        nslug = slugify(nm)
                        au, created = Author.objects.get_or_create(organization=org, slug=nslug, name=nm)
                        au.save()
                        create_copy(au, url, content, place)
                else:
                    nslug = slugify(name)
                    au, created = Author.objects.get_or_create(organization=org, slug=nslug, name=name)
                    create_copy(au, url, content, place)
            else:
                byline = pagesoup.findAll("a", {"rel": "author"})
                for by in byline:
                    name = by.text
                    nslug = slugify(name)
                    au, created = Author.objects.get_or_create(organization=org, slug=nslug, name=name)
                    create_copy(au, url, content, place)
def test_cases():
    do_work([{'href': 'http://www.huffingtonpost.com/2013/08/01/climate-change-and-violence_n_3692023.html'},
    {'href': 'http://www.huffingtonpost.com/2013/08/02/july-jobs-report-unemployment-rate_n_3690424.html'},
    {'href': 'http://www.huffingtonpost.com/2013/08/01/larry-summers-janet-yellen_n_3691052.html'},
    {'href': 'http://www.huffingtonpost.com/2013/08/01/larry-arnn-dark-ones-hillsdale_n_3691839.html'},
    {'href': 'http://www.huffingtonpost.com/2013/08/02/brian-williams-knee-replacement-surgery-temporary-medical-leave_n_3694732.html'},
    {'href': 'http://www.huffingtonpost.com/2013/08/01/colin-powell-affair_n_3691734.html'},
    {'href': 'http://www.huffingtonpost.com/2013/08/02/emily-gilbert-bob-filner_n_3695147.html'},
    {'href': 'http://www.huffingtonpost.com/2013/08/02/john-oliver-fast-food-workers_n_3695136.html'},
    {'href': 'http://www.huffingtonpost.com/2013/08/02/new-york-ag-big-bank-probe_n_3692564.html'}], 1)

class Command(BaseCommand):

    def handle(self, *args, **options):
        frontpage = requests.get("http://www.huffingtonpost.com/").content
        soup = BeautifulSoup(frontpage)
        divOInterest = soup.findAll("div", {"id": "center_entries"})
        splash = soup.findAll("div", {"id": "top_featured_news"})
        do_work(divOInterest[0].findAll("a"), 1)
        do_work(splash[0].findAll("a"), 0)
        #test_cases()


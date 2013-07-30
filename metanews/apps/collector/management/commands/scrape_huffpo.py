from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from metanews.apps.collector.models import Author, Copy
from BeautifulSoup import BeautifulSoup
import requests


def create_copy(author, url, content):
    copy, created = Copy.objects.get_or_create(url=url, slug=slugify(url))
    copy.text = content
    copy.save()
    author.copy.add(copy)

class Command(BaseCommand):

    def handle(self, *args, **options):
        frontpage = requests.get("http://www.huffingtonpost.com/").content
        soup = BeautifulSoup(frontpage)
        divOInterest = soup.findAll("div", {"id": "center_entries"})
        links = divOInterest[0].findAll("a")
        for link in links:
            url = link['href']
            if len(url.split("http://")) > 1:
                fn = slugify(url)
                print "getting url = %s" % url
                try:
                    with open("data/scrapes/huffpo/"+fn, "rb") as f:
                        content = f.read()
                except IOError:
                    page = requests.get(url)
                    with open("data/scrapes/huffpo/"+fn, "wb") as f:
                        f.write(page.content)
                        content = page.content
                pagesoup = BeautifulSoup(content)
                spans = pagesoup.findAll("span", "color_1A1A1A")
                if len(spans) == 1:
                    name = spans[0].text.split("By ")[1]
                    if len(name.split(' and ')) > 1:
                        for nm in name.split(' and '):
                            nslug = slugify(nm)
                            print nslug
                            au, created = Author.objects.get_or_create(slug=nslug, name=nm)
                            au.save()
                            create_copy(au, url, content)
                    else:
                        nslug = slugify(name)
                        print nslug
                        au, created = Author.objects.get_or_create(slug=nslug, name=name)
                        create_copy(au, url, content)

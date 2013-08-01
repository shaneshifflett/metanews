from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from metanews.apps.collector.models import Author, Article, Organization
from BeautifulSoup import BeautifulSoup
import itertools
import requests


def create_copy(author, url, content):
    copy, created = Article.objects.get_or_create(url=url)
    copy.text = content
    copy.save()
    author.articles.add(copy)

def clean_link(url):
    url = url.split("#")[0]
    url = url.split("?")[0]
    return url

class Command(BaseCommand):

    def handle(self, *args, **options):
        org, created = Organization.objects.get_or_create(name="The Huffington Post")
        frontpage = requests.get("http://www.huffingtonpost.com/").content
        soup = BeautifulSoup(frontpage)
        divOInterest = soup.findAll("div", {"id": "center_entries"})
        splash = soup.findAll("div", {"id": "top_featured_news"})
        links = itertools.chain(divOInterest[0].findAll("a"), splash[0].findAll("a"))
        for link in links:
            url = clean_link(link['href'])
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
                            au, created = Author.objects.get_or_create(organization=org, slug=nslug, name=nm)
                            au.save()
                            create_copy(au, url, content)
                    else:
                        nslug = slugify(name)
                        print nslug
                        au, created = Author.objects.get_or_create(organization=org, slug=nslug, name=name)
                        create_copy(au, url, content)

from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from metanews.apps.collector.models import Author, Article, Organization
from BeautifulSoup import BeautifulSoup
import itertools
import requests

org, created = Organization.objects.get_or_create(name="The New York Times")

def create_copy(author, url, content, place):
    copy, created = Article.objects.get_or_create(url=url)
    copy.text = content
    copy.featured_at = place
    try:
        copy.save()
    except Exception as e:
        import pdb; pdb.set_trace()
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
            print "getting url = %s" % url
            try:
                with open("data/scrapes/nytimes/"+fn, "rb") as f:
                    content = f.read()
            except IOError:
                page = requests.get(url)
                with open("data/scrapes/nytimes/"+fn, "wb") as f:
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
                        create_copy(au, url, content, place)
                else:
                    nslug = slugify(name)
                    print nslug
                    au, created = Author.objects.get_or_create(organization=org, slug=nslug, name=name)
                    create_copy(au, url, content, place)

class Command(BaseCommand):

    def handle(self, *args, **options):
        year = args[0]
        month = args[1]
        day = args[2]
        #use whowritesfor as a proxy for now
        frontpage = requests.get("http://whowritesfor.com/"+year+"/"+month+"/"+day).content
        soup = BeautifulSoup(frontpage)
        sexes = ['men', 'women']
        for sex in sexes:
            men = soup.findAll("div", {"class": sex})
            men_articles = men[0].findAll("div", {"class": "article"})
            for article in men_articles:
                name = article.find("h3").text
                nslug = slugify(name)
                url = clean_link(article.find("a")['href'])
                print "%s %s" % (nslug, url)
                content = requests.get(url).content
                au, created = Author.objects.get_or_create(organization=org, slug=nslug, name=name)
                create_copy(au, url, content, "1")

            
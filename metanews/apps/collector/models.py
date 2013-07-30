from django.db import models
from django_extensions.db.fields import AutoSlugField
from metanews.apps.classifier.genderPredictor import genderPredictor
from metanews.apps.classifier.gender import gender


class Organization(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=('name', ), overwrite=True)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    url = models.URLField()
    text = models.TextField(blank=True, null=True)
    date_scraped = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from=('url', ), overwrite=True)


class Author(models.Model):
    SEXES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    name = models.CharField(max_length=512)
    slug = AutoSlugField(populate_from=('name', ), overwrite=True)
    sex = models.CharField(max_length=1, choices=SEXES)
    articles = models.ManyToManyField(Article, blank=True, null=True,)
    date_created = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)

    def get_name_parts(self):
        return self.name.split(' ')

    def get_sex(self):
        name = self.get_name_parts()
        try:
            result = gender[name[0]]
        except KeyError:
            result = gp.classify(name[0])
        return result

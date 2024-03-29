from django.db import models
from django_extensions.db.fields import AutoSlugField
from metanews.apps.classifier.genderPredictor import genderPredictor
from metanews.apps.classifier.gender import gender


gp = genderPredictor()
conf = gp.trainAndTest()
print 'setting gp and conf'

class Organization(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=('name', ), overwrite=True)

    def __unicode__(self):
        return self.name

    def get_male_count(self):
        return Author.objects.filter(organization=self, sex="M").count()

    def get_female_count(self):
        return Author.objects.filter(organization=self, sex="F").count()

    def get_male_front_articles(self):
        front_splashes = 0
        auths = Author.objects.filter(organization=self, sex="M")
        for auth in auths:
            front_splashes += auth.articles.filter(featured_at=1).count()
        return front_splashes

    def get_female_front_articles(self):
        front_splashes = 0
        auths = Author.objects.filter(organization=self, sex="F")
        for auth in auths:
            front_splashes += auth.articles.filter(featured_at=1).count()
        return front_splashes


class Article(models.Model):
    PLACES = (
        ('0', 'splash'),
        ('1', 'front'),
        ('2', 'listview')
    )
    url = models.URLField()
    text = models.TextField(blank=True, null=True)
    date_scraped = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from=('url', ), overwrite=True)
    featured_at = models.CharField(max_length=1, choices=PLACES, blank=True, null=True, default="1")

    def featured_where(self):
        for place in self.PLACES:
            if place[0] == self.featured_at:
                return place[1]
        return ""


class Author(models.Model):
    SEXES = (
        ('M', 'male'),
        ('F', 'female')
    )
    name = models.CharField(max_length=512)
    slug = AutoSlugField(populate_from=('name', ), overwrite=True)
    sex = models.CharField(max_length=1, choices=SEXES, blank=True, null=True)
    sex_confidence = models.FloatField(default=1.0)
    articles = models.ManyToManyField(Article, blank=True, null=True,)
    date_created = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)

    def get_article_count(self):
        return self.articles.count()

    def get_splashed_article_count(self):
        return self.articles.filter(featured_at="0").count()

    def get_front_article_count(self):
        return self.articles.filter(featured_at="1").count()

    def get_name_parts(self):
        return self.name.split(' ')

    def set_sex(self):
        name = self.get_name_parts()
        try:
            result = gender[name[0]]
        except KeyError:
            result = gp.classify(name[0])
            self.sex_confidence = conf
        self.sex = self.SEXES[0][0] if result == 'male' else self.SEXES[1][0]
        self.save()
        return self.sex

    def get_sex(self):
        if self.sex is None:
            return self.set_sex()
        return self.sex

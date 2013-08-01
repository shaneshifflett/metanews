from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'metanews.apps.collector.views.home', name='home'),
    (r'^collector/', include('metanews.apps.collector.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

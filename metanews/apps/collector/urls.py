from django.conf.urls.defaults import *

from .views import AuthorListView, AuthorDetailView


urlpatterns = patterns('',
    url(r'detail/(?P<slug>.+)/$', AuthorDetailView.as_view(), name="author_detail"),
    url(r'^$', AuthorListView.as_view(), name="author_list"),
)
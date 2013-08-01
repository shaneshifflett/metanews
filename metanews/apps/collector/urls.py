from django.conf.urls.defaults import *

from .views import AuthorListView, AuthorDetailView, OrganizationListView


urlpatterns = patterns('',
    url(r'detail/(?P<slug>.+)/$', AuthorDetailView.as_view(), name="author_detail"),
    url(r'orgs/(?P<slug>.+)/$', AuthorListView.as_view(), name="author_list"),
    url(r'^$', OrganizationListView.as_view(), name="organization_list"),
)
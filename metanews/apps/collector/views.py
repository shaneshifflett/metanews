from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response
from django.template import RequestContext
from metanews.apps.collector.models import Author, Organization


def home(request, template='index.html'):
    context = {}
    return render_to_response(template, context, context_instance=RequestContext(request))


class OrganizationListView(ListView):
    context_object_name = 'organization_list'
    template_name = 'collector/orgs_list.html'
    queryset = Organization.objects.all()


class AuthorListView(ListView):
    context_object_name = 'author_list'
    template_name = 'collector/author_list.html'

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        self.queryset = Author.objects.filter(organization__slug=slug)
        return super(AuthorListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['org'] = kwargs['object_list'][0].organization if len(kwargs['object_list']) > 0 else None
        return context


class AuthorDetailView(DetailView):
    context_object_name = 'author'
    template_name = 'collector/author_detail.html'
    queryset = Author.objects.all()

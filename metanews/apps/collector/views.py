from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response
from django.template import RequestContext
from metanews.apps.collector.models import Author


def home(request, template='index.html'):
    context = {}
    return render_to_response(template, context, context_instance=RequestContext(request))


class AuthorListView(ListView):
    context_object_name = 'author_list'
    template_name = 'collector/author_list.html'
    queryset = Author.objects.all()


class AuthorDetailView(DetailView):
    context_object_name = 'author'
    template_name = 'collector/author_detail.html'
    queryset = Author.objects.all()

# -*- coding: utf-8 -*-
from django.views import generic
from django.views.generic.list_detail import object_list

from strona import models

class ArtykulyList(generic.ListView):
	model = models.Artykuly
	paginate_by = 1
	context_object_name = 'artykuly_list'
artykuly_list = ArtykulyList.as_view()

class ArtykulyDetailView(generic.DetailView):
    model = models.Artykuly
artykuly_detail = ArtykulyDetailView.as_view()

def aktualnosci_view(request, number):
	artykuly_list = models.Artykuly.objects.filter(categories=1)
	artykul_detail = models.Artykuly.objects.get(id__exact=number) 
	
	return object_list(request, queryset=artykuly_list,
		template_name= "strona/home_view.html",
		paginate_by = 4,
		extra_context={'artykul_detail': artykul_detail})

def hufiec_view(request, number):
	hufiec_list = models.Artykuly.objects.filter(categories=2).order_by('-posted_date')
	hufiec_detail = models.Artykuly.objects.get(id__exact=2)
	return object_list(request, queryset=hufiec_list,
		template_name= "strona/hufiec_view.html",
		extra_context={'hufiec_detail': hufiec_detail})



def druzyny_view(request, number):
	druzyny_list = models.Artykuly.objects.filter(categories=3)
	druzyny_detail = models.Artykuly.objects.get(id__exact=number)
	return object_list(request, queryset=druzyny_list,
		template_name= "strona/druzyny_view.html",
		extra_context={'druzyny_detail': druzyny_detail})

def rodzice_view(request, number):
	rodzice_list = models.Artykuly.objects.filter(categories=4)
	rodzice_detail = models.Artykuly.objects.get(id__exact=number) 
	return object_list(request, queryset=rodzice_list,
		template_name= "strona/rodzice_view.html",
		extra_context={'rodzice_detail': rodzice_detail})

class CategoryNewsList(ArtykulyList):
    template_name = 'strona/category_news_list.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryNewsList, self).get_context_data(**kwargs)
        context['category'] = self._get_category()
        return context

    def get_queryset(self):
        category = self._get_category()
        return models.Artykuly.objects.filter(categories=category)

    def _get_category(self):
        return models.Kategorie.objects.get(slug=self.kwargs['slug'])

category_news_list = CategoryNewsList.as_view()



# -*- coding: utf-8 -*-
from django.views import generic
from django.conf.urls.defaults import patterns, include, url

from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required

from strona import models

# robots.txt

# user
def login_user(request):
	if not request.user.is_authenticated():
		return django.contrib.auth.views.login(request, template_name='userpanel/login.html')
	else:
		return HttpResponseRedirect("/juser/")

def logout_then_login(request):
	return django.contrib.auth.views.logout_then_login(request, login_url = '/logout/')


# content
class ArtykulyList(generic.ListView):
	model = models.Artykuly
	paginate_by = 1
	context_object_name = 'artykuly_list'
artykuly_list = ArtykulyList.as_view()

class ArtykulyDetailView(generic.DetailView):
    model = models.Artykuly
artykuly_detail = ArtykulyDetailView.as_view()

class DruzynyList(generic.ListView):
	model = models.Druzyny
	context_object_name = 'druzyny_list'
druzyny_list = DruzynyList.as_view()

class DruzynyDetailView(generic.DetailView):
    model = models.Druzyny
druzyny_detail = DruzynyDetailView.as_view()


def aktualnosci_first(request):
	artykuly_list = models.Artykuly.objects.filter(categories=1).order_by('-posted_date')
	artykul_detail = models.Artykuly.objects.filter(categories=1).order_by("-id")[0]
	
	return object_list(request, queryset=artykuly_list,
		template_name= "strona/home_view.html",
		extra_context={'artykul_detail': artykul_detail})

def hufiec_first(request):
	hufiec_list = models.Artykuly.objects.filter(categories=2).order_by('-posted_date')
	hufiec_detail = models.Artykuly.objects.filter(categories=2).order_by("id")[0]

	return object_list(request, queryset=hufiec_list,
		template_name= "strona/hufiec_view.html",
		extra_context={'hufiec_detail': hufiec_detail})

def aktualnosci_view(request, number):
	artykuly_list = models.Artykuly.objects.filter(categories=1).order_by('-posted_date')
	artykul_detail = models.Artykuly.objects.get(id__exact=number) 
	
	return object_list(request, queryset=artykuly_list,
		template_name= "strona/home_view.html",
		paginate_by = 4,
		extra_context={'artykul_detail': artykul_detail})

def hufiec_view(request, number):
	hufiec_list = models.Artykuly.objects.filter(categories=2).order_by('-posted_date')
	hufiec_detail = models.Artykuly.objects.filter(categories=2).get(id__exact=number)
	return object_list(request, queryset=hufiec_list,
		template_name= "strona/hufiec_view.html",
		extra_context={'hufiec_detail': hufiec_detail})

def druzyny_view(request, slug):
	druzyny_list = models.Druzyny.objects.filter(dziala__gt=0).order_by('-nazwa')
	druzyny_detail = models.Druzyny.objects.get(slug__exact=slug)
	return object_list(request, queryset=druzyny_list,
		template_name= "strona/druzyny_view.html",
		extra_context={'druzyny_detail': druzyny_detail})

def rodzice_view(request, number):
	rodzice_list = models.Artykuly.objects.filter(categories=4)
	rodzice_detail = models.Artykuly.objects.get(id__exact=number) 
	return object_list(request, queryset=rodzice_list,
		template_name= "strona/rodzice_view.html",
		extra_context={'rodzice_detail': rodzice_detail})

def osoby_view(request, slug):
	dru_id = models.Druzyny.objects.filter(slug=slug)
	osoby_list = models.Osoby.objects.filter(dru=dru_id).order_by('-nazwisko')
	osoby_detail = models.Osoby.objects.get(id__exact=1)
	return object_list(request, queryset=osoby_list,
		template_name= "strona/osoby_view.html",
		extra_context={'osoby_detail': osoby_detail})

def osoby_detail(request, slug):
	dru_id = models.Druzyny.objects.filter(slug=slug)
	osoby_list = models.Osoby.objects.filter(dru=dru_id).order_by('-nazwisko')
	osoby_detail = models.Osoby.objects.get(id__exact=1)
	return object_list(request, queryset=osoby_list,
		template_name= "strona/osoby_view.html",
		extra_context={'osoby_detail': osoby_detail})


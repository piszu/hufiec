# -*- coding: utf-8 -*-

from django.views import generic
from django.conf.urls.defaults import patterns, include, url

from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from strona import models
from django import forms
from django.forms import ModelForm


####
# robots.txt
 
# user
def login_user(request):
	if not request.user.is_authenticated():
		return django.contrib.auth.views.login(request, template_name='userpanel/login.html')
	else:
		return HttpResponseRedirect("/accounts/login/")

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
	artykul_detail = models.Artykuly.objects.filter(categories=1).order_by('-posted_date')[0]
	return object_list(request, queryset=artykuly_list,
		template_name= "strona/home_view.html",
		paginate_by = 4,
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
	druzyny_list = models.Druzyny.objects.order_by('nazwa')
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

def mapa_wyjazdow(request):
	hufiec_list = models.Artykuly.objects.filter(categories=2).order_by('-posted_date')
	return object_list(request, queryset=hufiec_list,
		template_name= "strona/mapa_wyjazdow.html")

def profile_view(request):
	hufiec_list = models.Artykuly.objects.filter(categories=2).order_by('-posted_date')
	return object_list(request, queryset=hufiec_list,
		template_name= "strona/profile_view.html")

def osoby_view(request, slug):
	if request.user.is_authenticated():
		if slug == 'oplacenia':
				osoby_list = models.Osoby.objects.order_by('nazwisko')
		else:
			dru_id = models.Druzyny.objects.filter(slug=slug)
			osoby_list = models.Osoby.objects.filter(dru=dru_id).filter(aktywny=1).order_by('nazwisko')
			show = False
		return object_list(request, queryset=osoby_list,
			template_name= "strona/osoby_view.html",
			extra_context={'slug': slug , 'show': show })
	else:
		return HttpResponseRedirect("/accounts/login/")

def osoby_detail(request, slug, number):
	if request.user.is_authenticated():
		dru_id = models.Druzyny.objects.filter(slug=slug)
		show = True
		if slug == 'oplacenia':
			osoby_list = models.Osoby.objects.order_by('nazwisko')
		else:
			osoby_list = models.Osoby.objects.filter(dru=dru_id).filter(aktywny=1).order_by('nazwisko')
		osoby_detail = models.Osoby.objects.get(id__exact=number)
		query = ('''SELECT o.id, o.imie, o.nazwisko, SUM( w.kwota_wpl ) as wplata, s.rok, s.kwota_sk
					FROM szs_osoby o
					LEFT JOIN szs_wplaty w ON w.oso_id = o.id
					LEFT JOIN szs_skladki s ON w.skl_id = s.id
					WHERE o.id = %s 
					GROUP BY s.rok, o.imie, o.nazwisko ''')
		params = ( number )
		skladki_detail = models.Osoby.objects.raw(query, params)
		return object_list(request, queryset=osoby_list,
			template_name= "strona/osoby_view.html",
			extra_context={'osoby_detail': osoby_detail, 'skladki_detail': skladki_detail, 'show': show, 'slug': slug })
	else:
		return HttpResponseRedirect("/accounts/login/")


## wyszukiwanie osoby po PESEL
def person_search(request, slug):
	if request.user.is_authenticated():
		search = False
		druzyny_list = models.Druzyny.objects.filter(dziala__gt=0).order_by('-nazwa')
		druzyny_detail = models.Druzyny.objects.get(slug__exact=slug)
		person_find = None
		if 'pesel' in request.GET:
				qd = request.GET
				search = True
				try:
					person_find = models.Osoby.objects.filter( pesel__exact=qd.__getitem__('pesel') )
				except models.Osoby.DoesNotExist:
					person_find = None

		return object_list(request, queryset = druzyny_list,
			template_name= "strona/person_search.html",
			extra_context={'druzyny_detail': druzyny_detail , 'person_find': person_find, 'search': search} )
	else:
		return HttpResponseRedirect("/accounts/login/")


def person_assign(request, slug, number):
	if request.user.is_authenticated():
		osoba = models.Osoby.objects.get(id=number)
		druzyna = models.Druzyny.objects.get(slug=slug)
		osoba.dru_id = druzyna.id
		osoba.aktywny = 1
		osoba.save()
		osoba_list = models.Osoby.objects.filter(id=number)
		osoby_detail = models.Osoby.objects.get(id__exact=number)
		druzyny_detail = models.Druzyny.objects.get(slug__exact=slug)
		return object_list(request, queryset=osoba_list,
			template_name= "strona/person_assign.html",
			extra_context={'osoby_detail': osoby_detail, 'druzyny_detail': druzyny_detail,'slug': slug })
	else:
		return HttpResponseRedirect("/accounts/login/")

def person_del(request, slug, number):
	if request.user.is_authenticated():
		osoba = models.Osoby.objects.get(id=number)
		druzyna = models.Druzyny.objects.get(slug=slug)
		osoba.aktywny = 0
		osoba.save()
		osoba_list = models.Osoby.objects.filter(id=number)
		osoby_detail = models.Osoby.objects.get(id__exact=number)
		druzyny_detail = models.Druzyny.objects.get(slug__exact=slug)
		return object_list(request, queryset=osoba_list,
			template_name= "strona/person_del.html",
			extra_context={'osoby_detail': osoby_detail, 'druzyny_detail': druzyny_detail,'slug': slug })
	else:
		return HttpResponseRedirect("/accounts/login/")

def person_mod(request, slug, number):
	if request.user.is_authenticated():
		teamslug = slug
		osoba = models.Osoby.objects.get(id=number)
		if request.method == 'POST':
			form = ModPerson(request.POST, instance=osoba)
			if form.is_valid():
					form.save()
					return render_to_response('strona/person_mod.html', 
					{'form':form , 'teamslug': teamslug }, 
					context_instance = RequestContext(request),)
		else:      
			form = ModPerson(instance=osoba)
		return render_to_response('strona/person_mod.html', 
				{'form':form , 'teamslug': teamslug }, 
				context_instance=RequestContext(request) )
	else:
			return HttpResponseRedirect("/accounts/login/")

def person_add(request, slug):
	if request.user.is_authenticated():
		teamslug = slug
		if request.method == 'POST':
			form = AddPerson(request.POST)
			if form.is_valid():
				dru = models.Druzyny.objects.get(slug__exact=slug)
				fromdata = models.Osoby()
				fromdata.dru_id = dru.id
				fromdata.imie = form.cleaned_data.get('imie', 'imie')
				fromdata.nazwisko = form.cleaned_data.get('nazwisko', 'nazwisko')
				fromdata.pesel = form.cleaned_data.get('pesel', 'pesel')
				fromdata.telefon = form.cleaned_data.get('telefon', 'telefon')
				fromdata.m_urodzenia = form.cleaned_data.get('m_urodzenia', 'm_urodzenia')
				fromdata.aktywny = 1
				fromdata.slug = form.cleaned_data.get('slug', 'slug')			
				fromdata.uwagi = form.cleaned_data.get('uwagi', 'uwagi')
				fromdata.email = form.cleaned_data.get('email', 'email')			
				fromdata.save()
				form = AddPerson()
				return render_to_response('strona/person_add.html', 
				{'form':form , 'teamslug': teamslug }, 
				context_instance = RequestContext(request),)
		else:      
			form = AddPerson()
		return render_to_response('strona/person_add.html', 
				{'form':form , 'teamslug': teamslug }, 
				context_instance=RequestContext(request) )
	else:
			return HttpResponseRedirect("/accounts/login/")

	
def person_payment(request, slug, number):
	if request.user.is_authenticated():
		teamslug = slug
		if request.method == 'POST':
			skladki = PaymentForm(request.POST)
			if skladki.is_valid():
				oso = models.Osoby.objects.get(id__exact=number)
				fromdata = models.Wplaty()
				fromdata.oso_id = oso.id
				fromdata.skl = skladki.cleaned_data.get('skl', 'skl')
				fromdata.kwota_wpl = skladki.cleaned_data.get('kwota_wpl', 'kwota_wpl')
				fromdata.d_wplaty = skladki.cleaned_data.get('d_wplaty', 'd_wplaty')
				fromdata.uwagi = skladki.cleaned_data.get('uwagi', 'uwagi')
				fromdata.save()
				skladki = PaymentForm()
				return render_to_response('strona/person_payment.html', 
						{'skladki':skladki, 'teamslug': teamslug  }, 
						context_instance = RequestContext(request),)
		else:      
			skladki = PaymentForm()
		return render_to_response('strona/person_payment.html', 
				{'skladki':skladki, 'teamslug': teamslug  }, 
				context_instance=RequestContext(request) )
	else:
			return HttpResponseRedirect("/accounts/login/")


class AddPerson(ModelForm):
     class Meta:
         model = models.Osoby
         fields = ['imie', 'nazwisko', 'pesel', 'telefon', 'm_urodzenia', 'email', 'slug', 'uwagi' ]

class ModPerson(ModelForm):
     class Meta:
         model = models.Osoby
         fields = ['imie', 'nazwisko', 'pesel', 'telefon', 'm_urodzenia', 'email', 'uwagi' ]

class PaymentForm(ModelForm):
     class Meta:
         model = models.Wplaty
         fields = ['skl', 'kwota_wpl', 'd_wplaty', 'uwagi' ]





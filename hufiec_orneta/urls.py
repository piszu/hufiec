# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template, redirect_to
from strona.models import Artykuly
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	# robots.txt
  	url(r'^robots\.txt$', 'django.views.generic.simple.direct_to_template',
    {'template': 'robots.txt', 'mimetype': 'text/plain'}),
	# user
	url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
	url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
	url(r'^accounts/profile/$', 'strona.views.profile_view'),
	# panel administracyjny
	url(r'^administrator/', include(admin.site.urls)),
	#redirect na aktualności
    url(r'^/?$', redirect_to, {'url': '/a/'}),
	# aktualnosci
	url(r'^a/$', 'strona.views.aktualnosci_first', name='aktualnosci_first'), 
	url(r'^a/(?P<number>[0-9]+)/$', 'strona.views.aktualnosci_view', name='aktualnosci_view'), 
	# hufiec
	url(r'^h/$', 'strona.views.hufiec_first', name='hufiec_first'), 
	url(r'^h/(?P<number>[0-9]+)/$', 'strona.views.hufiec_view', name='hufiec_view'), 
	url(r'^h/mapa_wyjazdow/$', 'strona.views.mapa_wyjazdow', name='mapa_wyjazdow'), 

	# druzyny
	url(r'^d/(?P<slug>[\w\-_]+)/$', 'strona.views.druzyny_view', name='druzyny_view'),
	# osoby
	url(r'^d/(?P<slug>[\w\-_]+)/persons/$', 'strona.views.osoby_view', name='osoby_view'),
	url(r'^d/(?P<slug>[\w\-_]+)/add/$', 'strona.views.person_add', name='person_add'),
	url(r'^d/(?P<slug>[\w\-_]+)/search/$', 'strona.views.person_search', name='person_search'),
	url(r'^d/(?P<slug>[\w\-_]+)/del/(?P<number>[0-9]+)/$', 'strona.views.person_del', name='person_del'),
	url(r'^d/(?P<slug>[\w\-_]+)/mod/(?P<number>[0-9]+)/$', 'strona.views.person_mod', name='person_mod'),
	# widoki administracyjne
	# url(r'^d/kadra/$', 'strona.views.kadra_view', name='kadra_view'),
	url(r'^d/(?P<slug>[\w\-_]+)/pay/(?P<number>[0-9]+)/$', 'strona.views.person_payment', name='person_pay'),
	url(r'^d/(?P<slug>[\w\-_]+)/assign/(?P<number>[0-9]+)/$', 'strona.views.person_assign', name='person_assign'),
	url(r'^d/(?P<slug>[\w\-_]+)/persons/(?P<number>[0-9]+)/$', 'strona.views.osoby_detail', name='osoby_detail'),
	# wyszukiwanie osoby
    # url(r'^person_search/$', 'strona.views.person_search'),


	# rodzice
	url(r'^r/(?P<number>[0-9]+)/$', 'strona.views.rodzice_view', name='rodzice_view'), 
)


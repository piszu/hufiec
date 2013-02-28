# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to
from strona.models import Artykuly
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	# user
	url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
	url(r'^accounts/profile/$', 'django.contrib.auth.views.login'),
	# panel administracyjny
	url(r'^administrator/', include(admin.site.urls)),
	#redirect na aktualności
    url(r'^/?$', redirect_to, {'url': '/a/'}),
	# aktualnosc
	url(r'^a/$', 'strona.views.aktualnosci_first', name='aktualnosci_first'), 
	url(r'^a/(?P<number>[0-9]+)/$', 'strona.views.aktualnosci_view', name='aktualnosci_view'), 
	# hufiec
	url(r'^h/$', 'strona.views.hufiec_first', name='hufiec_first'), 
	url(r'^h/(?P<number>[0-9]+)/$', 'strona.views.hufiec_view', name='hufiec_view'), 
	# druzyny
	url(r'^d/(?P<number>[0-9]+)/$', 'strona.views.druzyny_view', name='druzyny_view'), 
	# rodzice
	url(r'^r/(?P<number>[0-9]+)/$', 'strona.views.rodzice_view', name='rodzice_view'), 
)


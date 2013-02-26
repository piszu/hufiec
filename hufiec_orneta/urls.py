# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to
from strona.models import Artykuly
from django.contrib import admin
admin.autodiscover()

info_dict = {
    'queryset': Artykuly.objects.filter(categories=1),
}

urlpatterns = patterns('',
	url(r'^page/(?P<page>[0-9]+)/$', 'strona.views.artykuly_list', name='artykuly-list'),
	url(r'^page/?$', 'strona.views.artykuly_list', name='artykuly-list'),
	url(r'^news/(?P<slug>[\w\-_]+)/$', 'strona.views.artykuly_detail', name='artykuly-detail'),
	url(r'^categories/(?P<slug>[\w\-_]+)/$', 'strona.views.category_news_list', name='category-news-list'),
	url(r'^categories/(?P<slug>[\w\-_]+)/(?P<page>[0-9]+)/$', 'strona.views.category_news_list', name='category-news-list'),
	url(r'^news/(?P<slug>[\w\-_]+)/$', 'strona.views.artykuly_detail', name='artykuly-detail'),


	# panel administracyjny
	url(r'^administrator/', include(admin.site.urls)),
    url(r'^/?$', redirect_to, {'url': '/a/1/'}),


	url(r'^a/(?P<number>[0-9]+)/$', 'strona.views.aktualnosci_view', name='aktualnosci_view'), # aktualnosci
	url(r'^h/$', 'strona.views.hufiec_view', name='hufiec_view'), # hufiec
	url(r'^h/(?P<number>[0-9]+)/$', 'strona.views.hufiec_view', name='hufiec_view'), # hufiec
	url(r'^d/(?P<number>[0-9]+)/$', 'strona.views.druzyny_view', name='druzyny_view'), # druzyny
	url(r'^r/(?P<number>[0-9]+)/$', 'strona.views.rodzice_view', name='rodzice_view'), # rodzice
)


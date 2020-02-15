"""dtc_bus_routes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from busroutes.views import (search_by_stage, search_by_num, stage_by_id, 
    bus_by_id, bus_by_stage, ajax_buses_from_here, ajax_bus_number_search,
    ajax_stage_search)

from api import urls as api_urls
from sitemaps import RouteSitemap, StageSitemap, StaticViewSitemap

sitemaps = {
    'routes': RouteSitemap,
    'stages': StageSitemap,
    'page_urls': StaticViewSitemap
}

handler500 = 'busroutes.views.server_error'

urlpatterns = [
    url(r'^api/', include(api_urls)),
    url(r'^admin/', admin.site.urls),

    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    url(r'^ads\.txt$', TemplateView.as_view(template_name='ads.txt', content_type='text/plain'), name='ads'),
    url(r'^manifest\.json$', TemplateView.as_view(template_name='manifest.json', content_type='application/json'), name='manifest'),
    url(r'^privacy/policy/$', TemplateView.as_view(template_name='privacypolicy.txt', content_type='text/plain'), name='privacypolicy'),

    url(r'^bus/route/search/$',search_by_stage,name='search_by_stage'),
    url(r'^bus/search/$',search_by_num,name='search_by_num'),
    url(r'^bus/stop/(?P<stop_id>\d+)/(?P<stop_name>.+)/$',stage_by_id,name='stage_by_id'),
    url(r'^bus/route/(?P<bus_id>\d+)/(?P<source>.+)/to/(?P<destination>.+)/$',bus_by_id,name='bus_by_id'),
    url(r'^bus/routes/from/(?P<source>.+)/to/(?P<destination>.+)/$',bus_by_stage,name='bus_by_stage'),
    url(r'^ajax/buses/from/here/$',ajax_buses_from_here,name='ajax_buses_from_here'),
    url(r'^ajax/bus/search/$',ajax_bus_number_search,name='ajax_bus_number_search'),
    url(r'^ajax/stage/search/$',ajax_stage_search,name='ajax_stage_search'),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url('__debug__/', include(debug_toolbar.urls)),
    ]

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

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', TemplateView.as_view(template_name="home.html"), name='home'),

    url(r'bus/route/search/$','busroutes.views.search_by_stage',name='search_by_stage'),
    url(r'bus/search/$','busroutes.views.search_by_num',name='search_by_num'),
  # url(r'stage/(?P<stageid>\d+)/$','buroutes.views.stage_by_id',name='stage_by_id')   #not implemented yet
    url(r'bus/route/(?P<bus_id>\d+)/(?P<source>.+)/to/(?P<destination>.+)/$','busroutes.views.bus_by_id',name='bus_by_id'),
    url(r'ajax/bus/$','busroutes.views.ajax_bus',name='ajax_bus'),
]

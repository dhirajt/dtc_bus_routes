# -*- coding: utf-8 -*-
from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^$', views.api_root, name='api_root'),
    url(r'^stages/$', views.stage_list, name='stage_list'),
    url(r'^stage/(?P<pk>[0-9]+)/$', views.stage_details, name='stage_details'),
    url(r'^search/stage/$', views.stage_search, name='stage_search'),
    url(r'^routes/$', views.route_list, name='route_list'),
    url(r'^route/(?P<pk>[0-9]+)/$', views.route_details, name='route_details'),
    url(r'^search/route/$', views.route_search, name='route_search'),
    url(r'^nearby/route/$', views.nearby_route, name='nearby_route'),

    url(r'^stage/eta/$', views.stage_eta, name='stage_eta'),
    url(r'^route/eta/$', views.route_eta, name='route_eta'),
]

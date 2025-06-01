# -*- coding: utf-8 -*-
from django.urls import re_path
from api import views

urlpatterns = [
    re_path(r'^$', views.api_root, name='api_root'),
    re_path(r'^stages/$', views.stage_list, name='stage_list'),
    re_path(r'^stage/(?P<pk>[0-9]+)/$', views.stage_details, name='stage_details'),
    re_path(r'^search/stage/$', views.stage_search, name='stage_search'),
    re_path(r'^routes/$', views.route_list, name='route_list'),
    re_path(r'^route/(?P<pk>[0-9]+)/$', views.route_details, name='route_details'),
    re_path(r'^route/planner/$', views.route_planner, name='route_planner'),
    re_path(r'^route/activity/feedback/(?P<route>[0-9]+)/$', views.route_activity_feedback, name='route_activity_feedback'),
    re_path(r'^search/route/$', views.route_search, name='route_search'),
    re_path(r'^nearby/route/$', views.nearby_route, name='nearby_route'),
    re_path(r'^firebase/topic/subscriptions/$', views.topic_subscriptions, name='topic_subscriptions'),

    re_path(r'^stage/eta/$', views.stage_eta, name='stage_eta'),
    re_path(r'^route/eta/$', views.route_eta, name='route_eta'),
]

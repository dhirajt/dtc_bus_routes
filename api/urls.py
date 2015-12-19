# -*- coding: utf-8 -*-
from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^stages/$', views.stage_list),
    url(r'^stage/(?P<s_id>[0-9]+)/$', views.stage_details),
]

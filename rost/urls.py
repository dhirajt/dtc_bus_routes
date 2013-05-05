from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'search/$','rost.views.search',name='search'),
    url(r'ajax/bus/$','rost.views.ajax_bus',name='ajax_bus'),
)


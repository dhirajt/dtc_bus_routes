from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'route/search/$','rost.views.search_by_stage',name='search_by_stage'),
    url(r'search/$','rost.views.search_by_num',name='search_by_num'),    
    url(r'ajax/bus/$','rost.views.ajax_bus',name='ajax_bus'),
)


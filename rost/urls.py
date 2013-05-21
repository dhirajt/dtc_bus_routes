from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'route/search/$','rost.views.searchbystg',name='searchstg'),
    url(r'search/$','rost.views.searchbynum',name='search'),    
    url(r'ajax/bus/$','rost.views.ajax_bus',name='ajax_bus'),
)


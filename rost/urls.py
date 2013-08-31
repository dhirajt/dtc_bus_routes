from django.conf.urls import patterns, url

urlpatterns = patterns('rost.views',

    url(r'route/search/$','search_by_stage',name='search_by_stage'),
    url(r'search/$','search_by_num',name='search_by_num'),
  # url(r'stage/(?P<stageid>\d+)/$','stage_by_id',name='stage_by_id')   #not implemented yet
    url(r'route/(?P<busid>\d+)/$','bus_by_id',name='bus_by_id'),
    url(r'ajax/bus/$','ajax_bus',name='ajax_bus'),
)


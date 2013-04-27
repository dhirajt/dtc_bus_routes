from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'search/$','rost.views.search',name='search'),
)


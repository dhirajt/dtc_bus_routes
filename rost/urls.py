from django.conf.urls import patterns, url

urlpatterns = patterns('',

    url(r'route/$', 'rost.views.route', name='route'),

)


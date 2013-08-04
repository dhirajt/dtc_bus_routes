from django.conf.urls import patterns, include, url

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

handler500 = 'rost.views.server_error'

urlpatterns = patterns('',

    url(r'^$', direct_to_template, {'template': 'home.html'}, name='home'),
    url(r'^bus/', include('rost.urls')),
    url(r'^robots\.txt$', direct_to_template, {'template': 'robots.txt',
                                               'mimetype': 'text/plain'}),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )


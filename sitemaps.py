# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from busroutes.models import Route


class RouteSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Route.objects.all()

    def lastmod(self, obj):
        return obj.last_modified


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return ['home', 'search_by_num', 'search_by_stage']

    def location(self, item):
        return reverse(item)

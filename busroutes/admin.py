# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from busroutes.models import Route, Stage, StageSequence


# Register your models here.
class RouteAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'start_stage', 'end_stage','show_url')
    search_fields = [ 'name', 'stages__name' ]
    ordering = ( 'name', )

    readonly_fields = ("show_url","name")

    def show_url(self, instance):
        response = u"""<a href="{0}" target='_blank'>{0}</a>""".format(
            instance.get_absolute_url())
        return mark_safe(response)
    show_url.short_description = "URL"


class StageAdmin(admin.ModelAdmin):
    list_display = ('name','name_slug','coordinates')
    search_fields = ['name', 'name_slug', 'coordinates']
    prepopulated_fields = {'name_slug': ('name',)}

    ordering = ('name',)

class StageSeqAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'stage', 'sequence',)
    search_fields = ['route__name', 'stage__name', 'sequence']
    ordering = ('route',)

admin.site.register(Route,RouteAdmin)
admin.site.register(Stage,StageAdmin)
admin.site.register(StageSequence,StageSeqAdmin)

# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from busroutes.models import Route, Stage, StageSequence


class StageAdmin(admin.ModelAdmin):
    list_display = ('name','name_slug','coordinates')
    search_fields = ['name', 'name_slug', 'coordinates']
    prepopulated_fields = {'name_slug': ('name',)}

    ordering = ('name',)

class StageSequenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'stage', 'sequence',)
    search_fields = ['route__name', 'stage__name', 'sequence']
    ordering = ('route',)

class StageSequenceAdminInline(admin.StackedInline):
    model = StageSequence

class RouteAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'start_stage', 'end_stage','show_url')
    search_fields = [ 'name', 'stages__name' ]
    ordering = ( 'name', )

    inlines = [
        StageSequenceAdminInline,
    ]

    readonly_fields = ("show_url",)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("name",)
        return self.readonly_fields

    def show_url(self, instance):
        response = u"""<a href="{0}" target='_blank'>{0}</a>""".format(
            instance.get_absolute_url())
        return mark_safe(response)
    show_url.short_description = "URL"


admin.site.register(Route,RouteAdmin)
admin.site.register(Stage,StageAdmin)
admin.site.register(StageSequence,StageSequenceAdmin)

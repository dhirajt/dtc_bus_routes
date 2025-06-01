# -*- coding: utf-8 -*-
import datetime
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.utils.safestring import mark_safe
from django.urls import reverse

from busroutes.models import (Route, Stage, StageSequence, MetroStation, 
    FirebaseNotification, FirebaseTopicSubscription)

class MetroStationsInline(admin.TabularInline):
    model = Stage.metro_stations.through

class MetroStationAdmin(GISModelAdmin):
    inlines = [
        MetroStationsInline,
    ]

    list_display = ('name','name_hindi', 'location', 'wiki_link', 'notes', 'station_details')
    search_fields = ['name', 'name_hindi', 'location', 'wiki_link', 'notes', 'station_details']

    ordering = ('name',)

class StageAdmin(GISModelAdmin):
    inlines = [
        MetroStationsInline,
    ]

    list_display = ('name','name_slug', 'location')
    search_fields = ['name', 'name_slug', 'location']
    prepopulated_fields = {'name_slug': ('name',)}

    ordering = ('name',)
    exclude = ('metro_stations',)

class StageSequenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'stage', 'sequence',)
    search_fields = ['route__name', 'stage__name', 'sequence']
    ordering = ('route',)

class StageSequenceAdminInline(admin.StackedInline):
    model = StageSequence
    min_num = 10

    def get_queryset(self, request):
        queryset = super(StageSequenceAdminInline, self).get_queryset(request)
        queryset = queryset.select_related('stage','route')
        return queryset
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(StageSequenceAdminInline, self).formfield_for_dbfield(db_field, **kwargs) 
        if db_field.name == 'stage':
            formfield.choices = formfield.choices
        return formfield

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


class FirebaseNotificationAdmin(admin.ModelAdmin):
    list_display = ('data', 'notification', 'fcm_options', 'tokens', 'created_at')
    search_fields = ['data', 'notification', 'fcm_options', 'tokens' ]
    ordering = ('created_at',)

    def get_changeform_initial_data(self, request):
        return {
            'data': {
                'NotificationIntentType': 'WEB/APP_HOME',
                'URL': '',
                'title': '',
                'body': '',
                'image_url': ''
            },
            'notification': {
                'title' : '',
                'body' : '',
                'image_url': '',
            },
            'topic' : '',
            'fcm_options' : {
                'analytics_label' : 'notif_' + datetime.datetime.now().strftime('%d%b%Y_%H%M%SPST')
            },
            'tokens': []
        }

class FirebaseTopicSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('instance_id', 'topic', 'created_at')
    search_fields = ['instance_id', 'topic', 'created_at']
    ordering = ('instance_id', 'created_at')

    
admin.site.register(Route,RouteAdmin)
admin.site.register(Stage,StageAdmin)
admin.site.register(StageSequence,StageSequenceAdmin)
admin.site.register(MetroStation,MetroStationAdmin)
admin.site.register(FirebaseNotification, FirebaseNotificationAdmin)
admin.site.register(FirebaseTopicSubscription, FirebaseTopicSubscriptionAdmin)

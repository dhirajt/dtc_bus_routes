# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager

class MetroStation(models.Model):
    name = models.CharField(max_length=64)
    name_hindi = models.CharField(max_length=64)
    wiki_link = models.URLField()
    station_details = JSONField()
    location = geomodels.PointField(default=Point(0, 0, srid=4326), srid=4326)
    notes = models.TextField(max_length=1000)

    class Meta:
        verbose_name = "Metro Station"
        verbose_name_plural = "Metro Stations"

    def __str__(self):
        return self.name

    @property
    def latitude(self):
        return self.location.y

    @property
    def longitude(self):
        return self.location.x


class Stage(models.Model):
    name = models.CharField(max_length=64)
    name_slug = models.SlugField(max_length=100)
    location = geomodels.PointField(default=Point(0, 0, srid=4326), srid=4326)
    uid = models.CharField(max_length=10,blank=True,default='')
    last_modified = models.DateTimeField(auto_now=True)
    metro_stations = models.ManyToManyField(MetroStation)

    aliases = TaggableManager(verbose_name='aliases', blank=True)
    
    class Meta:
        verbose_name = "Stage"
        verbose_name_plural = "Stages"

    def get_absolute_url(self):
        return reverse('stage_by_id', kwargs={
            'stop_id' : self.id,
            'stop_name':self.name_slug
        })

    @property
    def latitude(self):
        return self.location.y

    @property
    def longitude(self):
        return self.location.x

    @property
    def route_count(self):
        return StageSequence.objects.filter(stage_id=self.id).count()

    @property
    def routes(self):
        return list(StageSequence.objects.filter(stage_id=self.id).values_list('route__name', flat=True))

    def __str__(self):
        return self.name


class BusRouteTiming(models.Model):
    route = models.ForeignKey('Route', on_delete=models.DO_NOTHING)
    time = models.TimeField()
    is_ac = models.BooleanField()  # is air-conditioned

    class Meta:
        verbose_name = "Bus Route Timing"
        verbose_name_plural = "Bus Route Timings"

        unique_together=(('route','time','is_ac'),)


class Route(models.Model):
    DIRECTION_CHOICES = (
        ('U', 'Up'),
        ('D', 'Down'),
    )
    ROUTE_TYPE_CHOICES = (
        (1,'DTC'),
        (2,'Delhi Transit')
    )
    name = models.CharField(max_length=64)
    uid = models.CharField(max_length=50,blank=True,default='')

    aliases = TaggableManager(verbose_name='aliases',blank=True)

    start_stage = models.ForeignKey(Stage, related_name='start_stage', on_delete=models.DO_NOTHING)
    end_stage = models.ForeignKey(Stage, related_name='end_stage', on_delete=models.DO_NOTHING)
    direction = models.CharField(max_length=1,choices=DIRECTION_CHOICES,default='U')
    ac_bus_available = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)
    stages = models.ManyToManyField(
        Stage, through="StageSequence",through_fields=('route', 'stage'))
    route_type = models.IntegerField(choices=ROUTE_TYPE_CHOICES,default=1)
    frequency = models.IntegerField(default=-1)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Route"
        verbose_name_plural = "Routes"

        unique_together = (
            ('name','direction','route_type'),
            ('name', 'direction', 'start_stage','end_stage', 'route_type'),
        )

    def get_absolute_url(self):
        return reverse('bus_by_id',kwargs={
            'bus_id':self.id,
            'source':self.start_stage.name_slug,
            'destination':self.end_stage.name_slug
        })

    @property
    def stage_count(self):
        return self.stages.count()

    def __str__(self):
        return self.name

class RouteActivityFeedback(models.Model):
    RESPONSE_TYPE = (
        (0, "YES"),
        (1, "NO"),
        (2, "DON'T KNOW"),
    )
    route = models.ForeignKey(Route, on_delete=models.DO_NOTHING)
    response_type = models.IntegerField(choices=RESPONSE_TYPE, default=2)
    count = models.IntegerField()

    class Meta:
        unique_together = [['route', 'response_type']]

class StageSequence(models.Model):
    route = models.ForeignKey(Route, on_delete=models.DO_NOTHING)
    stage = models.ForeignKey(Stage, on_delete=models.DO_NOTHING)
    sequence = models.IntegerField()

    class Meta:
        verbose_name = "Stage Sequence"
        verbose_name_plural = "Stage Sequences"

        ordering = ['sequence']
        unique_together = (('route','stage','sequence'),)

    def __str__(self):
        return "Bus %s - %s. %s" % (self.route.name,str(self.sequence),str(self.stage.name))

class FirebaseNotification(models.Model):
    data = JSONField()
    notification = JSONField()
    fcm_options = JSONField()

    channel_id = models.TextField(max_length=1000, blank=True, null=True)
    topic = models.CharField(max_length=250, blank=True, null=True)

    tokens = JSONField(blank=True, null=True)

    sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Firebase Notification"
        verbose_name_plural = "Firebase Notifications"

    def __str__(self):
        return "Firebase Notification - %s" % (self.created_at.strftime('%d %b %Y'))

class FirebaseTopicSubscription(models.Model):
    instance_id = models.CharField(max_length=1000)
    topic = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Firebase Topic Subscription"
        verbose_name_plural = "Firebase Topic Subscription"

        unique_together = (('instance_id', 'topic'),)

    def __str__(self):
        return "Firebase Topic Subscription - %s...%s" % (self.instance_id[:20],self.instance_id[:10])

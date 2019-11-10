# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager
from geoposition.fields import GeopositionField


class Stage(models.Model):
    name = models.CharField(max_length=64)
    name_slug = models.SlugField(max_length=100)
    coordinates = GeopositionField()
    uid = models.CharField(max_length=10,blank=True,default='')
    last_modified = models.DateTimeField(auto_now=True)

    aliases = TaggableManager(verbose_name='aliases',blank=True)
    
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
        return self.coordinates.latitude

    @property
    def longitude(self):
        return self.coordinates.longitude

    def __unicode__(self):
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

    def __unicode__(self):
        return self.name + ' - ' + self.get_route_type_display()


class StageSequence(models.Model):
    route = models.ForeignKey(Route, on_delete=models.DO_NOTHING)
    stage = models.ForeignKey(Stage, on_delete=models.DO_NOTHING)
    sequence = models.IntegerField()

    class Meta:
        verbose_name = "Stage Sequence"
        verbose_name_plural = "Stage Sequences"

        ordering = ['sequence']
        unique_together = (('route','stage','sequence'),)

    def __unicode__(self):
        return "Bus %s - %s. %s" % (self.route.name,str(self.sequence),str(self.stage.name))

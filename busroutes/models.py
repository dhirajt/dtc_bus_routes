# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

from geoposition.fields import GeopositionField


class Stage(models.Model):
    name = models.CharField(max_length=64,unique=True)
    name_slug = models.SlugField(max_length=100)
    coordinates = GeopositionField()

    class Meta:
        verbose_name = "Stage"
        verbose_name_plural = "Stages"

    @property
    def latitude(self):
        return self.coordinates.latitude

    @property
    def longitude(self):
        return self.coordinates.longitude

    def __unicode__(self):
        return self.name


class BusRouteTiming(models.Model):
    route = models.ForeignKey('Route')
    time = models.TimeField()
    is_ac = models.BooleanField()  # is air-conditioned

    class Meta:
        verbose_name = "Bus Route Timing"
        verbose_name_plural = "Bus Route Timings"

        unique_together=(('route','time','is_ac'),)


class Route(models.Model):
    name = models.CharField(max_length=64)
    start_stage = models.ForeignKey(Stage, related_name='start_stage')
    end_stage = models.ForeignKey(Stage, related_name='end_stage')
    direction = models.CharField(max_length=4)  # up or down
    ac_bus_available = models.BooleanField(default=False)
    last_modified = models.DateTimeField(auto_now=True)
    stages = models.ManyToManyField(
        Stage, through="StageSequence",through_fields=('route', 'stage'))
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Route"
        verbose_name_plural = "Routes"

        unique_together = (('name','direction'),('name','start_stage','end_stage'),)

    def get_absolute_url(self):
        return reverse('bus_by_id',kwargs={
            'bus_id':self.id,
            'source':self.start_stage.name_slug,
            'destination':self.end_stage.name_slug
        })

    def __unicode__(self):
        return self.name


class StageSequence(models.Model):
    route = models.ForeignKey(Route)
    stage = models.ForeignKey(Stage)
    sequence = models.IntegerField()

    class Meta:
        verbose_name = "Stage Sequence"
        verbose_name_plural = "Stage Sequences"

        unique_together = (('route','stage','sequence'),)

    def __unicode__(self):
        return "Bus %s - %s. %s" % (self.route.name,str(self.sequence),str(self.stage.name))

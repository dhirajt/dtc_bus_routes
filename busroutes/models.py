# -*- coding: utf-8 -*-
from django.db import models
from geoposition.fields import GeopositionField


class Stage(models.Model):
    name = models.CharField(max_length=64,unique=True)
    name_slug = models.SlugField(max_length=100)
    coordinates = GeopositionField()

    class Meta:
        verbose_name = "Stage"
        verbose_name_plural = "Stages"

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
    stages = models.ManyToManyField(
        Stage, through="StageSequence",through_fields=('route', 'stage'))

    class Meta:
        verbose_name = "Route"
        verbose_name_plural = "Routes"

        unique_together = (('name','direction'),('name','start_stage','end_stage'),)

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
        return str(self.route.id)+' | '+str(self.stage.id)+'('+str(self.sequence)+')'

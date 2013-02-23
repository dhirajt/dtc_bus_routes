from django.db import models

class Stage(models.Model):
	name = models.CharField(max_length=64)
	lattitude = models.FloatField(null=True, blank=True)
	longitude = models.FloatField(null=True, blank=True)
	routes = models.ManyToManyField('Route')
	
	def __unicode__(self):
	    return self.name

class Route(models.Model):
	name = models.CharField(max_length=64)
	start = models.ForeignKey(Stage, related_name='start')
	end = models.ForeignKey(Stage, related_name='end')
	stages = models.ManyToManyField(Stage)
	
	def __unicode__(self):
	    return self.name

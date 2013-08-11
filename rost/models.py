from django.db import models

class Stage(models.Model):
    name = models.CharField(max_length=64)
    lattitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    routes = models.ManyToManyField('Route')

    def __unicode__(self):
        return self.name
    
    # This isn't correct! Uncomment this after implementing stage_by_id view func     
    #@models.permalink          
    #def get_absolute_url(self):
    #    return ('rost.views.bus_by_id',[self.id])


class Route(models.Model):
    name = models.CharField(max_length=64)
    start = models.ForeignKey(Stage, related_name='start')
    end = models.ForeignKey(Stage, related_name='end')
    stages = models.ManyToManyField(Stage, through="StageSeq")

    def __unicode__(self):
        return self.name


class StageSeq(models.Model):
    route = models.ForeignKey(Route)
    stage = models.ForeignKey(Stage)
    sequence = models.IntegerField()

    def __unicode__(self):
        return str(self.route.id)+' | '+str(self.stage.id)+'('
        +str(self.sequence)+')'


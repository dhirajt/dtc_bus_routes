from django.contrib import admin
from busroutes.models import Route, Stage, StageSequence


# Register your models here.
class RouteAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'start_stage', 'end_stage',)
    search_fields = [ 'name', 'stages__name' ]
    ordering = ( 'name', )

class StageAdmin(admin.ModelAdmin):
    list_display = ( 'name', )
    search_fields = [ 'name' ]
    ordering = ( 'name', )
    #readonly_fields = ("show_url",)   This is a mistake!
    '''
    def show_url(self, instance):
        url = reverse('bus_by_id', kwargs={"busid": instance.pk})
        response = """<a href="{0}"> {0} </a>""".format(url)
        return response
    show_url.allow_tags = True
    show_url.short_description = "Url of this stage"
    '''

class StageSeqAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'route', 'stage', 'sequence',)
    search_fields = [ 'route__name' ]
    ordering = ( 'route', )

admin.site.register(Route,RouteAdmin)
admin.site.register(Stage,StageAdmin)
admin.site.register(StageSequence,StageSeqAdmin)

from django.contrib import admin
from models import Stage, Route, StageSeq
from django.core.urlresolvers import reverse

class RouteAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'start', 'end',)
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
admin.site.register(StageSeq,StageSeqAdmin)

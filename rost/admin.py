from django.contrib import admin
from models import Stage, Route, StageSeq

class RouteAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'start', 'end',)
    search_fields = [ 'name', 'stages__name' ]
    ordering = ( 'name', )

class StageAdmin(admin.ModelAdmin):
    list_display = ( 'name', )
    search_fields = [ 'name' ]
    ordering = ( 'name', )
    
class StageSeqAdmin(admin.ModelAdmin):
    list_display = ( 'id', 'route', 'stage', 'sequence',)
    search_fields = [ 'route__name' ]
    ordering = ( 'route', )

admin.site.register(Route,RouteAdmin)
admin.site.register(Stage,StageAdmin)
admin.site.register(StageSeq,StageSeqAdmin)

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from models import Stage,Route,StageSeq

def home(request,error=None):
    return render(request,template_name="home.html")
      

def search(request):
    busno = request.GET['bus']
    try:
        obj = Route.objects.get(name=busno)
    except ObjectDoesNotExist:
        obj=None
        
    if obj:
        stops = StageSeq.objects.filter(route=obj.id).order_by('sequence')
        return render(request,"results.html",{"stops":stops,
               "first":stops[0].stage,"last":stops[len(stops)-1].stage,
               "route":busno})
    else :
        error = 'Bus not found!'
        return render(request,"home.html",{"error":error})
        
def ajax_bus(request):
    stop = request.GET.get('q');
    obj = Stage.objects.get(name=stop)
    route_list = '<b>Buses from here :</b> <br/>'+(
                 '<br />'.join([rout.name for rout in obj.routes.all()]))
    return HttpResponse(route_list)


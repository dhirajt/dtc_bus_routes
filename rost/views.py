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
        print obj
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


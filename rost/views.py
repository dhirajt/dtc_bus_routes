from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from models import Stage, Route, StageSeq

def server_error(request):
    return render(request,template_name="500.html")


def search_by_num(request):
    if request.GET:
        busno = request.GET['bus']
        try:
            obj = Route.objects.get(name=busno)
        except ObjectDoesNotExist:
            obj = None

        if obj:
            return HttpResponseRedirect(reverse('bus_by_id',args=(obj.id,)))
        else:
            error = 'Bus not found!'
            return render(request, "search_by_num.html", {"error": error})
    else:
        return render(request, "search_by_num.html")


def bus_by_id(request,busid=None):
    stops = StageSeq.objects.select_related().filter(
                 route=busid).order_by('sequence')
    if stops:
        return render(request, "results_by_num.html",
                          {"stops": stops,
                           "first": stops[0].stage,
                           "last": stops[len(stops)-1].stage,
                           "route": stops[0].route})
    else :
        raise Http404

def ajax_bus(request):
    stop = request.GET.get('q')
    obj = Stage.objects.get(name=stop)
    route_list = '<b>Buses from here :</b> <br/>'+(
                 '<br />'.join([rout.name for rout in obj.routes.all()]))
    return HttpResponse(route_list)


def search_by_stage(request):
    if request.GET:
        startstage = request.GET['startstage']
        endstage = request.GET['endstage']
        try:
            buses = Route.objects.filter(
                stages__name__icontains=startstage).filter(
                stages__name__icontains=endstage)
        except ObjectDoesNotExist:
            buses = None

        if buses:
            data,buslist = payloadmaker(buses, startstage, endstage)
            payload = {'startstage': startstage,
                       'endstage': endstage,
                       'data': data,
                       'buslist':buslist
                       }
            return render(request, "results_by_stage.html", payload)
        else:
            error = 'Either you entered wrong stop name or no direct route \
                 exists!'
            return render(request, "search_by_stage.html", {"error": error})

    else:
        return render(request, "search_by_stage.html")


def payloadmaker(buses, startstage, endstage):
    data = {}
    for bus in buses:
        stops = StageSeq.objects.select_related().filter(route__name=bus.name)
        x = stops.get(stage__name__icontains=startstage).sequence
        y = stops.get(stage__name__icontains=endstage).sequence
        stops = stops[min(x, y)-1:max(x, y)]
        data[bus.name] = [it.stage.name for it in stops]
        if data[bus.name][0] != startstage:
            data[bus.name].reverse()
        
    shortest = min(data,key=lambda item:len(data[item]))
    buslist = [shortest] + [ i for i in data.keys() if i!=shortest ]
    return (data,buslist)


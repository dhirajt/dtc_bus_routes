from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse as urlreverse
from django.core.exceptions import ObjectDoesNotExist

from models import Stage, Route, StageSeq


def home(request, error=None):
    return render(request, template_name="home.html")


def searchbynum(request):
    if request.GET:
        busno = request.GET['bus']
        try:
            obj = Route.objects.get(name=busno)
        except ObjectDoesNotExist:
            obj = None

        if obj:
            stops = StageSeq.objects.select_related().filter(
                route=obj.id).order_by('sequence')
            return render(request, "results.html",
                          {"stops": stops,
                           "first": stops[0].stage,
                           "last": stops[len(stops)-1].stage,
                           "route": busno})
        else:
            error = 'Bus not found!'
            return render(request, "searchbynum.html", {"error": error})
    else:
        return render(request, "searchbynum.html")


def ajax_bus(request):
    stop = request.GET.get('q')
    obj = Stage.objects.get(name=stop)
    route_list = '<b>Buses from here :</b> <br/>'+(
                 '<br />'.join([rout.name for rout in obj.routes.all()]))
    return HttpResponse(route_list)


def searchbystg(request):
    if request.GET:
        startstg = request.GET['startstg']
        endstg = request.GET['endstg']
        try:
            buses = Route.objects.filter(
                stages__name__icontains=startstg).filter(
                stages__name__icontains=endstg)
        except ObjectDoesNotExist:
            buses = None

        if buses:
            data,buslist = payloadmaker(buses, startstg, endstg)
            payload = {'startstg': startstg,
                       'endstg': endstg,
                       'data': data,
                       'buslist':buslist
                       }
            return render(request, "resultsstg.html", payload)
        else:
            error = 'Either you entered wrong stop name or no direct route \
                 exists!'
            return render(request, "searchbystg.html", {"error": error})

    else:
        return render(request, "searchbystg.html")


def payloadmaker(buses, startstg, endstg):
    data = {}
    for bus in buses:
        stops = StageSeq.objects.select_related().filter(route__name=bus.name)
        x = stops.get(stage__name__icontains=startstg).sequence
        y = stops.get(stage__name__icontains=endstg).sequence
        stops = stops[min(x, y)-1:max(x, y)]
        data[bus.name] = [it.stage.name for it in stops]
        if data[bus.name][0] != startstg:
            data[bus.name].reverse()
        
    shortest=max(data,key=len)
    buslist = [shortest] + [ i for i in data.keys() if i!=shortest ]
    return (data,buslist)


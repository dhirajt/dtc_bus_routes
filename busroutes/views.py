import pickle

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from models import Stage, Route, StageSequence

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
            return redirect(
                'bus_by_id', bus_id=obj.id, source=obj.start_stage.name_slug,
                destination=obj.end_stage.name_slug)
        else:
            error = 'Bus not found!'
            return render(request, "search_by_num.html", {"error": error})
    else:
        return render(request, "search_by_num.html")


def bus_by_id(request,bus_id=None,source='',destination=''):
    stops = list(StageSequence.objects.select_related().filter(
                 route=bus_id).order_by('sequence'))
    if not stops:
        raise Http404

    source_stage = stops[0].stage.name_slug
    destination_stage  = stops[len(stops)-1].stage.name_slug

    if source!=source_stage or destination!=destination_stage:
        return redirect('bus_by_id',bus_id=bus_id,source=source_stage,destination=destination_stage)

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
    route_names = list(obj.route_set.values_list('name',flat=True))
    route_list = '<b>Buses from here :</b> <br/>'+(
                 '<br />'.join(route_names))
    return HttpResponse(route_list)


def search_by_stage(request):
    if request.GET:
        startstage = request.GET['startstage']
        endstage = request.GET['endstage']
        try:
            buses = Route.objects.filter(
                stages__name=startstage).filter(
                stages__name=endstage)
        except ObjectDoesNotExist:
            buses = None

        if buses:
            data_payload = payloadmaker(buses, startstage, endstage)
            payload = {'startstage': startstage,
                       'endstage': endstage,
                       'data': data_payload,
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
        stops = list(StageSequence.objects.select_related().filter(
            route__name=bus.name).order_by('sequence'))

        start_stage = [i for i in stops if i.stage.name == startstage][0]
        end_stage = [i for i in stops if i.stage.name == endstage][0]

        x = stops.index(start_stage)
        y = stops.index(end_stage)

        if y<x:
            x,y = y,x

        stops = stops[x:y+1]

        data[bus.name] = [it.stage.name for it in stops]
        if data[bus.name][0] != startstage:
            data[bus.name].reverse()

    shortest = min(data,key=lambda item:len(data[item]))
    buslist = [shortest] + [ i for i in data.keys() if i!=shortest ]
    payload = [(bus,data[bus]) for bus in buslist]
    return payload

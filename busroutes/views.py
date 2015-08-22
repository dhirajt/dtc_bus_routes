# -*- coding: utf-8 -*-
import json
import redis

from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
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
                           "startstage": stops[0].stage,
                           "endstage": stops[len(stops)-1].stage,
                           "route": stops[0].route})
    else :
        raise Http404

def ajax_buses_from_here(request):
    stop = request.GET.get('q')
    obj = Stage.objects.get(name=stop)
    route_names = list(obj.route_set.values_list('name',flat=True))
    route_list = '<b>Buses from here :</b> <br/>'+(
                 '<br />'.join(route_names))
    return HttpResponse(route_list)

def ajax_bus_number_search(request):
    if not request.is_ajax():
        return HttpResponseBadRequest
    query = request.GET.get('q','')
    buses = []

    if query:
        rclient = redis.StrictRedis(connection_pool=settings.BUS_REDIS_POOL)
        buses = rclient.smembers(query)
        if not buses:
            buses = list(Route.objects.filter(name__istartswith=query).values_list('name',flat=True))
            if buses:
                rclient.sadd(query,*buses)
                rclient.expire(query,6*60*60)
    return HttpResponse("\n".join(buses))

def ajax_stage_search(request):
    if not request.is_ajax():
        return HttpResponseBadRequest
    query = request.GET.get('q','')
    stages = []
    if query:
        rclient = redis.StrictRedis(connection_pool=settings.STAGE_REDIS_POOL)
        stages = rclient.smembers(query)
        if not stages:
            stages = list(Stage.objects.filter(name__istartswith=query).values_list('name',flat=True))
            if stages:
                rclient.sadd(query,*stages)
                rclient.expire(query,6*60*60)
    return HttpResponse("\n".join(stages))

def bus_by_stages(request,source='',destination=''):
    buses = Route.objects.filter(
            stages__name_slug=source).filter(
            stages__name_slug=destination)

    if buses.exists():
        startstage = Stage.objects.get(name_slug=source)
        endstage =  Stage.objects.get(name_slug=destination)

        data_payload = payloadmaker(buses, source, destination)
        payload = {
            'startstage': startstage.name,
            'endstage': endstage.name,
            'data': data_payload,
        }
        return render(request, "results_by_stage.html", payload)
    else:
        return redirect('search_by_stage')

def search_by_stage(request):
    if request.GET:
        startstage = request.GET['startstage']
        endstage = request.GET['endstage']
        buses = Route.objects.filter(
                stages__name=startstage).filter(
                stages__name=endstage)

        buses_exist = buses.exists()
        source = list(Stage.objects.filter(name=startstage))
        destination =  list(Stage.objects.filter(name=endstage))

        if buses_exist and source and destination:
            return redirect('bus_by_stage',source=source[0].name_slug,
                destination=destination[0].name_slug)
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

        start_stage = [i for i in stops if i.stage.name_slug == startstage][0]
        end_stage = [i for i in stops if i.stage.name_slug == endstage][0]

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

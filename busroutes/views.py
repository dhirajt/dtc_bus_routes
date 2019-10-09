# -*- coding: utf-8 -*-
import json
import redis

from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.db.models import Prefetch
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
        route_type = 1
        if ' - Cluster' in busno:
            route_type = 2
            busno = busno.split(' - ')[0]

        try:
            obj = Route.objects.get(name=busno,route_type=route_type)
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
    stops = list(StageSequence.objects.select_related().filter(route=bus_id).order_by('sequence'))
    if not stops:
        raise Http404

    source_stage = stops[0].stage.name_slug
    destination_stage  = stops[len(stops)-1].stage.name_slug

    if source!=source_stage or destination!=destination_stage:
        return redirect('bus_by_id',bus_id=bus_id,source=source_stage,destination=destination_stage)

    rclient = redis.StrictRedis(connection_pool=settings.API_CACHE_REDIS_POOL)
    access_token = rclient.get('access_token')

    if stops:
        return render(request, "results_by_num.html",
                          {"stops": stops,
                           "startstage": stops[0].stage,
                           "endstage": stops[len(stops)-1].stage,
                           "route": stops[0].route,
                           "access_token": access_token})
    else :
        raise Http404

def stage_by_id(request, stop_id=None, stop_name=''):
    stage = Stage.objects.get(id=stop_id)
    if not stage:
        raise Http404

    if stop_name != stage.name_slug:
        return redirect('bus_by_id', bus_id=stop_id, stop_name=stop_name_slug)

    rclient = redis.StrictRedis(connection_pool=settings.API_CACHE_REDIS_POOL)
    access_token = rclient.get('access_token')

    routes = stage.route_set.prefetch_related(
        Prefetch('stages', queryset=Stage.objects.only('name'))).all()
    stages = [list(route.stages.only('name')) for route in routes]
    route_values = list(routes.values_list(
        'id', 'name', 'start_stage__name', 'end_stage__name', 'start_stage__name_slug', 'end_stage__name_slug'))

    payload = []
    for index, route in enumerate(route_values):
        payload.append({
            'id': route[0],
            'name': route[1],
            'start_stage_name': route[2],
            'end_stage_name': route[3],
            'start_stage_slug': route[4],
            'end_stage_slug': route[5],
            'stages': stages[index] 
        })

    if routes:
        return render(request, "stage_by_id.html", {
            "routes": payload,
            "stage": stage
        })

def ajax_buses_from_here(request):
    stop_id = request.GET.get('id')
    obj = Stage.objects.get(id=stop_id)
    route_names = list(obj.route_set.filter(is_active=True).values_list('name',flat=True))
    route_names = sorted(route_names)
    route_list = '<b>Buses from here :</b> <br/>'+(
                 '<br />'.join(route_names))
    return HttpResponse(route_list)

def ajax_bus_number_search(request):
    if not request.is_ajax():
        return HttpResponseBadRequest
    query = request.GET.get('q','')
    bus_names = []

    if query:
        rclient = redis.StrictRedis(connection_pool=settings.BUS_REDIS_POOL)
        bus_names = rclient.smembers(query)
        bus_names = sorted(bus_names)
        if not bus_names:
            buses = list(Route.objects.filter(name__icontains=query).values_list('name','route_type'))
            bus_names = [item[0] if item[1] == 1 else item[0] + ' - Cluster' for item in buses]
            if bus_names:
                bus_names = sorted(bus_names)
                rclient.sadd(query,*bus_names)
                rclient.expire(query,6*60*60)
    return HttpResponse("\n".join(bus_names))

def ajax_stage_search(request):
    if not request.is_ajax():
        return HttpResponseBadRequest
    query = request.GET.get('q','')
    stages = []
    if query:
        rclient = redis.StrictRedis(connection_pool=settings.STAGE_REDIS_POOL)
        stages = rclient.smembers(query)
        stages = sorted(stages)
        if not stages:
            stages = list(Stage.objects.filter(name__icontains=query).values_list('name',flat=True))
            if stages:
                stages = sorted(stages)
                rclient.sadd(query,*stages)
                rclient.expire(query,6*60*60)
    return HttpResponse("\n".join(stages))

def bus_by_stage(request,source='',destination=''):
    direct_buses = Route.objects.filter(
            is_active=True,
            stages__name_slug=source).filter(stages__name_slug=destination)

    stages = list(Stage.objects.filter(name_slug__in=[source,destination]))

    startstage = [item for item in stages if item.name_slug == source]
    endstage = [item for item in stages if item.name_slug == destination]

    if startstage:
        startstage = startstage[0]
    if endstage:
        endstage = endstage[0]

    payload = None
    if startstage and endstage and direct_buses.exists():
        payload = direct_route_finder(direct_buses, startstage, endstage)
        context = {
            'direct_routes':payload,
            'startstage': startstage.name,
            'endstage': endstage.name
        }
    elif startstage and endstage:
        payload = indirect_route_finder(startstage,endstage)
        context = {
            'indirect_routes':payload,
            'startstage': startstage.name,
            'endstage': endstage.name
        }
    if not payload:
        url = reverse('search_by_stage') + '?redirect_error=true'
        return redirect(url)
    return render(request, "results_by_stage.html", context)

def search_by_stage(request):
    if request.GET:
        redirect_error = request.GET.get('redirect_error',None)
        startstage = request.GET.get('startstage','')
        endstage = request.GET.get('endstage','')

        source = list(Stage.objects.filter(name=startstage))
        destination =  list(Stage.objects.filter(name=endstage))

        if source and destination and not redirect_error:
            return redirect('bus_by_stage',source=source[0].name_slug,
                destination=destination[0].name_slug)
        else:
            error = 'Either you entered wrong stop name or no route exists!'
            return render(request, "search_by_stage.html", {"error": error})

    else:
        return render(request, "search_by_stage.html")

def direct_route_finder(buses, startstage, endstage):
    data = {}
    for bus in buses:
        stops = list(StageSequence.objects.select_related().filter(
            route__name=bus.name).order_by('sequence'))

        start_stage = [i for i in stops if i.stage.name_slug == startstage.name_slug][0]
        end_stage = [i for i in stops if i.stage.name_slug == endstage.name_slug][0]

        x = stops.index(start_stage)
        y = stops.index(end_stage)

        if y<x:
            x,y = y,x

        stops = stops[x:y+1]

        stagelist = [it.stage.name for it in stops]

        if stagelist[0] != startstage.name:
            stagelist.reverse()

        data[bus.name] = stagelist
    payload = sorted(data.items(),key=lambda item:len(item[1]))
    return payload

def indirect_route_finder(startstage=None,endstage=None):
	if not (startstage and endstage):
		return []

	routes_start = list(Route.objects.filter(stages=startstage,is_active=True).prefetch_related(
		Prefetch('stages',queryset=Stage.objects.all().order_by('stagesequence__sequence'))).all())
	routes_end = list(Route.objects.filter(stages=endstage,is_active=True).prefetch_related(
		Prefetch('stages',queryset=Stage.objects.all().order_by('stagesequence__sequence'))).all())

	route_list = []

	for rs in routes_start:
		for re in routes_end:
			stages_rs = list(rs.stages.all())
			stages_re = list(re.stages.all())

			changeovers = list(set(stages_rs) & set(stages_re))

			if changeovers:
				index_startstage = stages_rs.index(startstage)
				index_endstage = stages_re.index(endstage)

				potential_changeovers = [
					(stages_rs.index(item),abs(index_startstage - stages_rs.index(item))) for item in changeovers]

				potential_changeovers = sorted(potential_changeovers,key=lambda item:item[1])

				first_changeover_index_rs = potential_changeovers[0][0]
				first_changeover = stages_rs[first_changeover_index_rs]

				start_stages = []
				if first_changeover_index_rs > index_startstage:
					start_stages = stages_rs[index_startstage:first_changeover_index_rs+1]
				else:
					start_stages = stages_rs[first_changeover_index_rs:index_startstage+1]
					start_stages.reverse()

				end_stages = []
				first_changeover_index_re = stages_re.index(first_changeover)
				if first_changeover_index_re > index_endstage:
					end_stages = stages_re[index_endstage:first_changeover_index_re+1]
					end_stages.reverse()
				else:
					end_stages = stages_re[first_changeover_index_re:index_endstage+1]

				indirect_route = {
					'start_stages':{
						'route': rs,
						'stages': start_stages
					},
					'end_stages': {
						'route': re,
						'stages': end_stages
					},
					'changeover':first_changeover
				}
				route_list.append(indirect_route)
	route_list.sort(key=lambda item:len(item['start_stages']['stages'])+len(item['end_stages']['stages']))
	return route_list

# -*- coding: utf-8 -*-
import json
import os
import re
import redis
import requests
import uuid

from .aesencryption import AesCrypt256

from collections import OrderedDict, Counter
from .serializers import (StageBasicSerializer, StageAdvancedSerializer,
    RouteBasicSerializer, RouteAdvancedETASerializer, StageETASerializer,
    StageETAListSerializer, VehicleSerializer, RouteAdvancedSerializer,
    NearbyRouteSerializer, RoutePlannerSerializer, RouteActivityFeedbackSerializer,
    FirebaseTopicSubscriptionSerializer)

from rest_framework.request import Request
from rest_framework.exceptions import NotFound, ParseError, ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings

from django.db.models import F, Q
from django.db.models import Prefetch

from django.contrib.gis.geos import Polygon, Point

from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from geopy.distance import distance
from busroutes.models import Stage, Route, StageSequence, RouteActivityFeedback
from .responses import BusRoutesStandardResponse


aescrypt = AesCrypt256()
KEY = os.getenv('ENDPOINT_KEY','')

def get_final_endpoint(endpoint_name='',payload=''):
    BASE_ENDPOINT = os.getenv('BASE_ENDPOINT','')
    endpoint_dict = {
        'stage_eta' : os.getenv('STAGE_ETA_ENDPOINT',''),
        'route_eta' : os.getenv('ROUTE_ETA_ENDPOINT','')
    }
    aid = uuid.uuid4().hex[:16]
    endpoint_path = endpoint_dict.get(endpoint_name,'')

    url = BASE_ENDPOINT + aescrypt.encryptB64URLSafe(
        KEY, ';'.join([endpoint_path+aid,payload]))

    rclient = redis.StrictRedis(connection_pool=settings.API_CACHE_REDIS_POOL)
    proxies = {}
    proxy_list = rclient.lrange('proxies', 0, -1)
    if proxy_list:
        proxies['http'] = proxy_list[0]

    return url, proxies

def get_endpoint_headers():
    headers = {
        'User-Agent': os.getenv('ENDPOINT_UA',''),
        'Host': os.getenv('ENDPOINT_HOST',''),
        'Connection': os.getenv('ENDPOINT_CONNECTION',''),
        'Accept-Encoding': os.getenv('ENDPOINT_AE',''),
    }
    return headers

def get_paginated_response(queryset,request,serailizer):
    pagination_class = getattr(api_settings,'DEFAULT_PAGINATION_CLASS',None)
    if not pagination_class:
        serialized_obj = serailizer(
            paginated_queryset,
            many=True,
            context={'request': request})
        return Response(serialized_obj)
    else:
        paginator = pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset,request)

        serialized_obj = serailizer(
            paginated_queryset,
            many=True,
            context={'request': request})

        response_data = OrderedDict([
            ('data_count', paginator.page.paginator.count),
            ('page_count', paginator.page.paginator.num_pages),
            ('next', paginator.get_next_link()),
            ('previous', paginator.get_previous_link()),
            ('results', serialized_obj.data)
        ])

        return BusRoutesStandardResponse(response_data)

@api_view(['POST'])
def topic_subscriptions(request):
    if request.method == 'POST':
        serializer = FirebaseTopicSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return BusRoutesStandardResponse(serializer.data, status=status.HTTP_201_CREATED)
        return BusRoutesStandardResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def stage_list(request):
    """
    Returns all the stages in bus route database.
    """
    viewportne = request.query_params.get('viewportne', None)
    viewportsw = request.query_params.get('viewportsw', None)
    location = request.query_params.get('location', None)
    filter_expression = Q()

    if viewportsw and viewportne:
        ne_latlng = list(map(float, viewportne.strip().split(',')))
        sw_latlng = list(map(float, viewportsw.strip().split(',')))

        polygon = Polygon.from_bbox((
            min(ne_latlng[1], sw_latlng[1]),min(ne_latlng[0], sw_latlng[0]),
            max(ne_latlng[1], sw_latlng[1]),max(ne_latlng[0], sw_latlng[0])))

        filter_expression.add(Q(location__contained=polygon), Q.AND)

    if location:
        lat, lng = location.strip().split(',')
        location = Point(float(lng.strip()), float(lat.strip()), srid=4326)

    stages = None
    if location:
        stages = Stage.objects.filter(filter_expression).prefetch_related('metro_stations').annotate(
            distance=Distance('location', location)).order_by("distance")
    else:
        stages = Stage.objects.filter(filter_expression).prefetch_related('metro_stations').order_by('pk')

    response = get_paginated_response(
        stages,
        request,
        StageAdvancedSerializer)
    return response


@api_view(['GET'])
def stage_details(request,pk):
    """
    Returns all the stages in bus route database.
    """
    try:
        stage = Stage.objects.get(pk=pk)
    except Stage.DoesNotExist:
        raise NotFound()

    serializer = StageAdvancedSerializer(
        stage,
        context={'request': request})
    return BusRoutesStandardResponse(serializer.data)

@api_view(['GET'])
def stage_search(request):
    """
    Search for a stage in bus route database.
    """
    name = request.GET.get('name','')
    if not name:
        raise ParseError()

    location = request.query_params.get('location', None)

    if location:
        lat, lng = location.strip().split(',')
        location = Point(float(lng.strip()), float(lat.strip()), srid=4326)

    if location:
        stages = Stage.objects.filter(name__icontains=name).annotate(distance=Distance('location', location))
    else:
        stages = Stage.objects.filter(name__icontains=name)

    serializer = StageAdvancedSerializer(
        stages,
        many=True,
        context={'request': request})

    response_data = {
        'count': len(serializer.data),
        'results':serializer.data
    }
    return BusRoutesStandardResponse(response_data)

@api_view(['GET'])
def route_list(request):
    """
    Returns all the routes in bus route database.
    """
    stages = Route.objects.select_related('start_stage','end_stage').all().order_by('pk')
    response = get_paginated_response(
        stages,
        request,
        RouteBasicSerializer)
    return response

# @cache_page(60*60*24)
# @vary_on_cookie
@api_view(['GET'])
def nearby_route(request):
    """
    Returns all the routes in the nearby area.
    """
    viewportne = request.query_params.get('viewportne', None)
    viewportsw = request.query_params.get('viewportsw', None)
    location = request.query_params.get('location', None)
    filter_expression = Q()

    if not viewportsw or not viewportne:
        raise ValidationError('Both viewportsw and viewportne must be sent to get nearby routes.')

    if location:
        lat, lng = location.strip().split(',')
        location = Point(float(lng.strip()), float(lat.strip()), srid=4326)

    ne_latlng = list(map(float, viewportne.strip().split(',')))
    sw_latlng = list(map(float, viewportsw.strip().split(',')))

    polygon = Polygon.from_bbox((
        min(ne_latlng[1], sw_latlng[1]),min(ne_latlng[0], sw_latlng[0]),
        max(ne_latlng[1], sw_latlng[1]),max(ne_latlng[0], sw_latlng[0])))

    route_sequences = list(StageSequence.objects.filter(
        stage__location__contained=polygon).select_related().prefetch_related().values('stage__location', 'stage__name', 'stage__id', 
            'route__name', 'route__id', 'route__route_type', 'route__start_stage__name', 'route__end_stage__name'))

    stage_ids = set([])
    route_ids = set([])

    for route_seq in route_sequences:
        stage_ids.add(route_seq['stage__id'])
        route_ids.add(route_seq['route__id'])

    bus_counts = Counter(StageSequence.objects.filter(stage_id__in=stage_ids).values_list('stage_id', flat=True))
    route_counts = Counter(StageSequence.objects.filter(route_id__in=route_ids).values_list('route_id', flat=True))

    nearby_routes = {}
    nearby_stages = {}
    route_types = dict(Route.ROUTE_TYPE_CHOICES)

    for route_seq in route_sequences:
        if route_seq['stage__id'] not in nearby_stages:
            nearby_stages[route_seq['stage__id']] = {
                'stage': route_seq['stage__name'],
                'stage_id': route_seq['stage__id'],
                'latitude': route_seq['stage__location'].coords[1],
                'longitude': route_seq['stage__location'].coords[0],
                #'distance': distance(reversed(route_seq['stage__location'].coords), reversed(location.coords)).meters,
                'distance' : route_seq['stage__location'].distance(location) * 100000 if location else None,
                'bus_count': bus_counts[route_seq['stage__id']]
            }
        if route_seq['route__id'] not in nearby_routes:
            nearby_routes[route_seq['route__id']] = {
                'route': route_seq['route__name'],
                'route_id': route_seq['route__id'],
                'start_stage': route_seq['route__start_stage__name'],
                'end_stage': route_seq['route__end_stage__name'],
                'route_type': route_types[route_seq['route__route_type']],
                'stage_count': route_counts[route_seq['route__id']],
                'stages': []
            }
        nearby_routes[route_seq['route__id']]['stages'].append(nearby_stages[route_seq['stage__id']])
        nearby_routes[route_seq['route__id']]['stages'] = sorted(nearby_routes[route_seq['route__id']]['stages'], key=lambda item: item['distance'])

    data = sorted(list(nearby_routes.values()), key=lambda item: min([i['distance'] for i in item['stages']]))

    serializer = NearbyRouteSerializer(data, many=True, context={'request': request})
    return BusRoutesStandardResponse(serializer.data)

# @cache_page(60*60*24*5)
# @vary_on_cookie
@api_view(['GET'])
def route_details(request,pk):
    """
    Returns all the stages in bus route database.
    """
    # routes = Route.objects.filter(
    #         pk=pk,is_active=True).select_related('start_stage','end_stage').prefetch_related(
    #             Prefetch('stages',queryset=Stage.objects.all().order_by('stagesequence__sequence')))

    # if not routes:
    #     raise NotFound()

    # serializer = RouteAdvancedSerializer(
    #     routes,
    #     many=True,
    #     context={'request': request})

    try:
        route = Route.objects.prefetch_related('stages').get(pk=pk,is_active=True)
    except Route.DoesNotExist:
        raise NotFound()

    serializer = RouteAdvancedSerializer(
        route,
        context={'request': request})

    return BusRoutesStandardResponse(serializer.data)

@api_view(['GET', 'POST'])
def route_activity_feedback(request, route):
    """
    Sets/Returns all the feedback collected for a route.
    """
    try:
        route = Route.objects.get(id=route)
    except Route.DoesNotExist:
        raise NotFound()

    if request.method == 'GET':
        try:
            feedback_list = RouteActivityFeedback.objects.filter(route=route)
        except RouteActivityFeedback.DoesNotExist:
            return NotFound()
        serializer = RouteActivityFeedbackSerializer(
            feedback_list, many=True, context={'request': request})
        return BusRoutesStandardResponse(serializer.data)

    elif request.method == 'POST':
        response_type = request.data.get('response_type', -1)

        if response_type > -1:
            feedback, created = RouteActivityFeedback.objects.get_or_create(
                route=route, response_type=response_type, defaults={"count" : 0})
            feedback.count = F('count') + 1
            feedback.save()
        else:
            return ParseError()
        return BusRoutesStandardResponse(None)

# @cache_page(60*60*24*5)
# @vary_on_cookie
@api_view(['GET'])
def route_planner(request):
    """
    Plan a trip.
    """
    from_stage = request.GET.get('from_stage','')
    to_stage = request.GET.get('to_stage','')

    if not from_stage or not to_stage:
        return ParseError()

    try:
        start_stage = Stage.objects.get(id=from_stage)
    except Stage.DoesNotExist:
        return ParseError()

    try:
        end_stage = Stage.objects.get(id=to_stage)
    except Stage.DoesNotExist:
        return ParseError()

    final_payload = {
        'from_stage': start_stage,
        'to_stage': end_stage,
        'itineraries': []
    }

    direct_routes = direct_routes_payload(start_stage, end_stage)
    for item in direct_routes:
        final_payload['itineraries'].append({
            'legs' : [{
                'leg_type': 'TRANSIT',
                'trip_leg': item
            }]
        })

    if not final_payload['itineraries']:
        direct_buses = set([item['route'].id for item in direct_routes])
        indirect_routes = indirect_routes_payload(start_stage, end_stage, direct_buses)
        
        for item in indirect_routes:
            final_payload['itineraries'].append({
                'legs' : [{
                    'leg_type': 'TRANSIT',
                    'trip_leg': item[0]
                }, {
                    'leg_type': 'TRANSIT',
                    'trip_leg': item[1]
                }]
            })
    if final_payload['itineraries']:
        final_payload['itineraries'][0]['recommended'] = True

    serializer = RoutePlannerSerializer(
        final_payload,
        context={'request': request})

    return BusRoutesStandardResponse(serializer.data)

def direct_routes_payload(start_stage, end_stage):
    start_stage_routes = StageSequence.objects.filter(stage_id=start_stage).values_list('route__id', flat=True)
    direct_buses = list(StageSequence.objects.filter(
            route__id__in=start_stage_routes).filter(stage_id=end_stage).values_list('route__id', flat=True))
    
    data = {}
    for bus in direct_buses:
        direction = None
        stops = list(StageSequence.objects.select_related().filter(route_id=bus).order_by('sequence'))

        start_stage_idx = -1
        end_stage_idx = -1
        for index, stop in enumerate(stops):
            if stop.stage.id == start_stage.id:
                start_stage_idx = index
            elif stop.stage.id == end_stage.id:
                end_stage_idx = index

        final_stops = []
        if end_stage_idx < start_stage_idx:
            direction = stops[0].stage
            final_stops = stops[end_stage_idx:start_stage_idx+1]
            final_stops.reverse()
        else:
            direction = stops[-1].stage
            final_stops = stops[start_stage_idx:end_stage_idx+1]

        first_stop_with_coordinates = None
        last_stop_with_coordinates = None
        for stop in final_stops:
            if stop.stage.latitude < 1 or stop.stage.longitude < 1:
                continue

            if not first_stop_with_coordinates:
                first_stop_with_coordinates = stop.stage
            last_stop_with_coordinates = stop.stage


        data[bus] = {
            'route': Route.objects.get(id=bus),
            'leg_type': "TRANSIT",
            'start_stage': final_stops[0].stage,
            'end_stage': final_stops[-1].stage,
            'direction': direction,
            'num_stops': len(final_stops),
            'stops': [item.stage for item in final_stops],
            'fare': get_fare_estimate(first_stop_with_coordinates.location.distance(last_stop_with_coordinates.location) * 100)
        }

    payload = list(sorted(data.values(), key=lambda item:(len(item['stops']), item['fare'])))
    return payload

def indirect_routes_payload(start_stage, end_stage, direct_buses):
    if not (start_stage and end_stage):
        return []

    routes_start = list(Route.objects.filter(stages=start_stage, is_active=True).prefetch_related(
        Prefetch('stages', queryset=Stage.objects.all().order_by('stagesequence__sequence'))).all())
    routes_end = list(Route.objects.filter(stages=end_stage, is_active=True).prefetch_related(
        Prefetch('stages', queryset=Stage.objects.all().order_by('stagesequence__sequence'))).all())

    routes_start = [item for item in routes_start if item.id not in direct_buses]
    routes_end = [item for item in routes_end if item.id not in direct_buses]

    itineraries = []
    for rs in routes_start:
        for re in routes_end:
            direction_rs = None
            direction_re = None
            stages_rs = list(rs.stages.all())
            stages_re = list(re.stages.all())

            changeovers = list(set(stages_rs) & set(stages_re))

            if changeovers:
                index_startstage = stages_rs.index(start_stage)
                index_endstage = stages_re.index(end_stage)

                potential_changeovers = [
                    (stages_rs.index(item),abs(index_startstage - stages_rs.index(item))) for item in changeovers]

                potential_changeovers = sorted(potential_changeovers,key=lambda item:item[1])

                first_changeover_index_rs = potential_changeovers[0][0]
                first_changeover = stages_rs[first_changeover_index_rs]

                start_stages = []
                if first_changeover_index_rs > index_startstage:
                    direction_rs = stages_rs[-1]
                    start_stages = stages_rs[index_startstage:first_changeover_index_rs+1]
                else:
                    direction_rs = stages_rs[0]
                    start_stages = stages_rs[first_changeover_index_rs:index_startstage+1]
                    start_stages.reverse()

                end_stages = []
                first_changeover_index_re = stages_re.index(first_changeover)
                if first_changeover_index_re > index_endstage:
                    direction_re = stages_re[0]
                    end_stages = stages_re[index_endstage:first_changeover_index_re+1]
                    end_stages.reverse()
                else:
                    direction_re = stages_re[-1]
                    end_stages = stages_re[first_changeover_index_re:index_endstage+1]

                first_stop_with_coordinates_start = None
                last_stop_with_coordinates_start = None
                for stop in start_stages:
                    if stop.latitude < 1 or stop.longitude < 1:
                        continue

                    if not first_stop_with_coordinates_start:
                        first_stop_with_coordinates_start = stop
                    last_stop_with_coordinates_start = stop

                first_stop_with_coordinates_end = None
                last_stop_with_coordinates_end = None
                for stop in end_stages:
                    if stop.latitude < 1 or stop.longitude < 1:
                        continue

                    if not first_stop_with_coordinates_end:
                        first_stop_with_coordinates_end = stop
                    last_stop_with_coordinates_end = stop

                itinerary = [{
                    'route': rs,
                    'leg_type': "TRANSIT",
                    'start_stage': start_stages[0],
                    'end_stage': start_stages[-1],
                    'num_stops': len(start_stages),
                    'direction': direction_rs,
                    'stops': start_stages,
                    'fare': get_fare_estimate(first_stop_with_coordinates_start.location.distance(last_stop_with_coordinates_start.location) * 100)
                }, {
                    'route': re,
                    'leg_type': "TRANSIT",
                    'start_stage': end_stages[0],
                    'end_stage': end_stages[-1],
                    'num_stops': len(end_stages),
                    'direction': direction_re,
                    'stops': end_stages,
                    'fare': get_fare_estimate(first_stop_with_coordinates_end.location.distance(last_stop_with_coordinates_end.location) * 100)
                }]

                itineraries.append(itinerary)
    itineraries.sort(key=lambda item:(item[0]['num_stops'] + item[-1]['num_stops'], item[0]['fare'] + item[-1]['fare']))
    return itineraries

@api_view(['GET'])
def route_search(request):
    """
    Search for a stage in bus route database.
    """
    name = request.GET.get('name','')
    if not name:
        raise ParseError()

    routes = Route.objects.filter(
        name__icontains=name,is_active=True).select_related('start_stage','end_stage').prefetch_related(
            Prefetch('stages',queryset=Stage.objects.all().order_by('stagesequence__sequence'))).order_by('name')

    serializer = RouteBasicSerializer(
        routes,
        many=True,
        context={'request': request})

    response_data = {
        'count': len(serializer.data),
        'results':serializer.data
    }
    return BusRoutesStandardResponse(response_data)

@api_view(['GET'])
def stage_eta(request):
    """
    Get eta of buses on a stage.
    """
    stage_id = request.GET.get('stage_id','')
    if not stage_id:
        raise ParseError()

    if stage_id.isdigit():
        stages = list(Stage.objects.filter(
            Q(uid=stage_id) | Q(id=stage_id)))
    else:
        stages = list(Stage.objects.filter(uid=stage_id))

    if not stages:
        raise NotFound()

    stage_id = stages[0].uid

    eta_list = []

    rclient = redis.StrictRedis(connection_pool=settings.API_CACHE_REDIS_POOL)
    cached_eta_list = rclient.get('stage_eta:'+stage_id)
    if cached_eta_list:
        eta_list = json.loads(cached_eta_list)
    else:
        url, proxies = get_final_endpoint(
            endpoint_name='stage_eta',payload=stage_id)
        headers = get_endpoint_headers()

        response = requests.get(url, proxies=proxies)

        if response.ok:
            response_json_text = aescrypt.decryptB64(KEY,response.text)
            try:
                response_json = json.loads(response_json_text)
            except ValueError:
                response_json = ''

            if response_json and response_json['etaList']:
                for item in response_json['etaList']:
                    seat_availability = 'Unknown'
                    if 'available' in item['occupancy'].lower():
                        seat_availability = 'Available'

                    bus_type = 'DTC'
                    if item['typeOfBuses'] == '8':
                        bus_type = 'Cluster'

                    passengers = None
                    if item['passengers'].isdigit():
                        passengers = int(item['passengers'])

                    latitude = None
                    longitude = None

                    eta_list.append({
                        'passengers': passengers,
                        'destination': item['destination'],
                        'route_id': item['routeId'],
                        'eta_minutes': int(item['eta']),
                        'location': item['location'],
                        'bus_number': item['busno'],
                        'seat_availability':seat_availability,
                        'bus_type': bus_type,
                        'latitude': latitude,
                        'longitude': longitude
                    })
    if eta_list:
        rclient.setex('stage_eta:'+stage_id, 30, json.dumps(eta_list))

    eta_serializer = StageETAListSerializer(
        eta_list,
        many=True,
        context={'request': request})

    serializer = StageETASerializer(
        stages,
        many=True,
        context={'request': request, 'eta_list':eta_serializer})

    return BusRoutesStandardResponse(serializer.data)


@api_view(['GET'])
def route_eta(request):
    """
    Get eta of buses on a route.
    """
    route_id = request.GET.get('route_id','')
    stage_id = request.GET.get('stage_id','')

    if not route_id:
        raise ParseError()

    if route_id.isdigit():
        routes = list(Route.objects.filter(
            Q(uid=route_id) | Q(id=route_id)))
    else:
        routes = list(Route.objects.filter(uid=route_id))

    if not routes:
        raise NotFound()

    route = routes[0]
    route_id = route.uid

    eta_list = []

    rclient = redis.StrictRedis(connection_pool=settings.API_CACHE_REDIS_POOL)
    cached_data = rclient.get('route_eta:'+route_id)

    data = {}
    if cached_data:
        data = json.loads(cached_data)
    else:
        url, proxies = get_final_endpoint(
            endpoint_name='route_eta',payload=route_id)
        headers = get_endpoint_headers()

        response = requests.get(url, proxies=proxies)

        if response.ok:
            response_json_text = aescrypt.decryptB64(KEY,response.text)
            try:
                response_json = json.loads(response_json_text)
            except ValueError:
                response_json = ''

            vehicle_list = []
            eta_list = []

            if response_json and response_json['vehicleList']:
                for item in response_json['vehicleList']:
                    if item['vehicleNo']:
                        vehicle_number, extra_text = item['vehicleNo'].strip().split(' ',1)

                        location, seat_availability = extra_text.split(
                            '\n')[1].split(', ')

                        if 'available' in seat_availability:
                            seat_availability = 'Available'

                        vehicle_list.append({
                            'location': location,
                            'latitude': item['latitude'],
                            'longitude': item['longitude'],
                            'seat_availability': seat_availability,
                            'vehicle_number': vehicle_number
                        })

            if response_json and response_json['allBusStops']:
                for item in response_json['allBusStops']:
                    seat_availability = 'Unknown'
                    if item['occupancy'] and 'available' in item['occupancy'].lower():
                        seat_availability = 'Available'

                    passengers = None
                    if item['passengers'] and item['passengers'].isdigit():
                        passengers = int(item['passengers'])

                    latitude = item['latitude']
                    longitude = item['longitude']

                    eta_minutes = None

                    name_split = item['Name'].strip().split('\n',1)
                    if len(name_split) > 1:
                        eta_minutes = list(map(
                            int,re.findall('(\d+)',name_split[1])))

                    eta_list.append({
                        'passengers': passengers,
                        'eta_minutes': eta_minutes,
                        'seat_availability':seat_availability,
                        # 'latitude': latitude,
                        # 'longitude': longitude,
                        'name': name_split[0]
                    })

            data['vehicle_list'] = vehicle_list
            data['eta_list'] = eta_list

    if any(data.values()):
        rclient.setex('route_eta:'+route_id, 30, json.dumps(data))

    vehicle_serializer = VehicleSerializer(
        data['vehicle_list'],
        many=True,
        context={'request': request})

    serializer = RouteAdvancedETASerializer(
        route,
        context={'request': request, 'vehicle_list':vehicle_serializer})

    final_serialized_data = serializer.data
    if final_serialized_data and final_serialized_data["stages"]:
        zipped_data = list(zip(final_serialized_data["stages"],data['eta_list']))

        if zipped_data:
            for index,item in enumerate(final_serialized_data["stages"]):
                if len(zipped_data[index]) > 1:
                    final_serialized_data["stages"][index] = OrderedDict(
                        list(final_serialized_data["stages"][index].items())+list(zipped_data[index][1].items()))

    return BusRoutesStandardResponse(final_serialized_data)

def get_fare_estimate(distance):
    if 0 < distance < 4:
        return 5
    elif 4 <= distance < 10:
        return 10
    else:
        return 15

@api_view(('GET','POST'))
@permission_classes((AllowAny, ))
def api_root(request, format=None):
    return Response(OrderedDict([
        ('stages', reverse('stage_list', request=request, format=format)),
        ('stage', reverse('stage_details', request=request, kwargs={'pk':1}, format=format)),
        ('stage_search', reverse('stage_search', request=request, format=format)),
        ('routes', reverse('route_list', request=request, format=format)),
        ('route_planner', reverse('route_planner', request=request, format=format)),
        ('route', reverse('route_details', request=request, kwargs={'pk':1}, format=format)),
        ('route_activity_feedback', reverse('route_activity_feedback', request=request, kwargs={'route':1}, format=format)),
        ('route_search', reverse('route_search', request=request, format=format)),
        ('stage_eta', reverse('stage_eta', request=request, format=format)),
        ('route_eta', reverse('route_eta', request=request, format=format)),
        ('nearby_route', reverse('nearby_route', request=request, format=format)),
        ('topic_subscriptions', reverse('topic_subscriptions', request=request, format=format)),
    ]))

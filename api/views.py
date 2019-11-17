# -*- coding: utf-8 -*-
import json
import os
import re
import redis
import requests
import uuid

from .aesencryption import AesCrypt256

from collections import OrderedDict
from .serializers import (StageBasicSerializer, StageAdvancedSerializer,
    RouteBasicSerializer, RouteAdvancedETASerializer, StageETASerializer,
    StageETAListSerializer, VehicleSerializer, RouteAdvancedSerializer,
    NearbyRouteSearializer)

from rest_framework.request import Request
from rest_framework.exceptions import NotFound, ParseError, ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings

from django.db.models import Q
from django.db.models import Prefetch

from django.contrib.gis.geos import Polygon, Point

from django.conf import settings
from geopy.distance import distance
from busroutes.models import Stage, Route, StageSequence
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

@api_view(['GET'])
def stage_list(request):
    """
    Returns all the stages in bus route database.
    """
    viewportne = request.query_params.get('viewportne', None)
    viewportsw = request.query_params.get('viewportsw', None)
    filter_expression = Q()

    if viewportsw and viewportne:
        ne_latlng = list(map(float, viewportne.strip().split(',')))
        sw_latlng = list(map(float, viewportsw.strip().split(',')))

        polygon = Polygon.from_bbox((
            min(ne_latlng[1], sw_latlng[1]),min(ne_latlng[0], sw_latlng[0]),
            max(ne_latlng[1], sw_latlng[1]),max(ne_latlng[0], sw_latlng[0])))

        filter_expression.add(Q(location__contained=polygon), Q.AND)

    stages = Stage.objects.filter(filter_expression).order_by('pk')
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

    stages = list(Stage.objects.filter(name__icontains=name))

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
        stage__location__contained=polygon).values('stage__location', 'stage__name', 'stage__id', 
            'route__name', 'route__id', 'route__route_type', 'route__start_stage__name', 'route__end_stage__name'))

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
                'distance': distance(reversed(route_seq['stage__location'].coords), reversed(location.coords)).meters,
                #'distace' : route_seq['stage__location'].distance(location) * 100000 if location else None,
                'bus_count': StageSequence.objects.filter(stage_id=route_seq['stage__id']).count()
            }
        if route_seq['route__id'] not in nearby_routes:
            nearby_routes[route_seq['route__id']] = {
                'route': route_seq['route__name'],
                'route_id': route_seq['route__id'],
                'start_stage': route_seq['route__start_stage__name'],
                'end_stage': route_seq['route__end_stage__name'],
                'route_type': route_types[route_seq['route__route_type']],
                'stages': []
            }
        nearby_routes[route_seq['route__id']]['stages'].append(nearby_stages[route_seq['stage__id']])

    data = sorted(list(nearby_routes.values()), key=lambda item: min([i['distance'] for i in item['stages']]))

    serializer = NearbyRouteSearializer(data, many=True, context={'request': request})
    return BusRoutesStandardResponse(serializer.data)

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
        route = Route.objects.get(pk=pk,is_active=True)
    except Route.DoesNotExist:
        raise NotFound()

    serializer = RouteAdvancedSerializer(
        route,
        context={'request': request})

    return BusRoutesStandardResponse(serializer.data)

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

@api_view(('GET',))
@permission_classes((AllowAny, ))
def api_root(request, format=None):
    return Response(OrderedDict([
        ('stages', reverse('stage_list', request=request, format=format)),
        ('stage', reverse('stage_details', request=request, kwargs={'pk':1}, format=format)),
        ('stage_search', reverse('stage_search', request=request, format=format)),
        ('routes', reverse('route_list', request=request, format=format)),
        ('route', reverse('route_details', request=request, kwargs={'pk':1}, format=format)),
        ('route_search', reverse('route_search', request=request, format=format)),
        ('stage_eta', reverse('stage_eta', request=request, format=format)),
        ('route_eta', reverse('route_eta', request=request, format=format)),
        ('nearby_route', reverse('nearby_route', request=request, format=format))
    ]))

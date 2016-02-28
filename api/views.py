# -*- coding: utf-8 -*-
from collections import OrderedDict
from serializers import (StageBasicSerializer, StageAdvancedSerializer,
    RouteBasicSerializer, RouteAdvancedSerializer)

from rest_framework.request import Request
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings

from django.db.models import Prefetch
from busroutes.models import Stage, Route
from .responses import BusRoutesStandardResponse


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
    stages = Stage.objects.all()
    response = get_paginated_response(
        stages,
        request,
        StageBasicSerializer)
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
        [stage],
        many=True,
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
    stages = Route.objects.select_related('start_stage','end_stage').all()
    response = get_paginated_response(
        stages,
        request,
        RouteBasicSerializer)
    return response

@api_view(['GET'])
def route_details(request,pk):
    """
    Returns all the stages in bus route database.
    """
    routes = Route.objects.filter(
            pk=pk,is_active=True).select_related('start_stage','end_stage').prefetch_related(
                Prefetch('stages',queryset=Stage.objects.all().order_by('stagesequence__sequence')))

    if not routes:
        raise NotFound()

    serializer = RouteAdvancedSerializer(
        routes,
        many=True,
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
    ]))

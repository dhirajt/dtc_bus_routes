# -*- coding: utf-8 -*-
from serializers import StageBasicSerializer,StageAdvancedSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response

from busroutes.models import Stage

@api_view(['GET'])
def stage_list(request):
    """
    Returns all the stages in bus route database.
    """
    stages = Stage.objects.all()
    serializer = StageBasicSerializer(stages, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def stage_details(request,s_id):
    """
    Returns all the stages in bus route database.
    """
    stage = Stage.objects.filter(id=s_id)
    serializer = StageAdvancedSerializer(stage, many=True)
    return Response(serializer.data)

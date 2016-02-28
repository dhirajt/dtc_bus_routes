# -*- coding: utf-8 -*-
from rest_framework import serializers
from busroutes.models import Stage, Route, StageSequence

class StageBasicSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='stage_details')
    class Meta:
        model = Stage
        fields = ('id', 'name', 'url')

class StageAdvancedSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='stage_details')
    class Meta:
        model = Stage
        fields = ('id', 'name', 'name_slug', 'latitude', 'longitude','url')


class RouteBasicSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='route_details')

    start_stage = StageBasicSerializer()
    end_stage = StageBasicSerializer()

    class Meta:
        model = Route
        fields = ('id', 'name', 'url', 'start_stage','end_stage')

class RouteAdvancedSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='route_details')

    start_stage = StageBasicSerializer()
    end_stage = StageBasicSerializer()

    stages = StageAdvancedSerializer(many=True)

    class Meta:
        model = Route
        fields = ('id', 'name', 'url', 'start_stage','end_stage','stages')

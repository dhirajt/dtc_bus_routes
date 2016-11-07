# -*- coding: utf-8 -*-
from rest_framework import serializers
from busroutes.models import Stage, Route, StageSequence


class ETASerializer(serializers.Serializer):
    eta_minutes = serializers.IntegerField()
    passengers = serializers.IntegerField(allow_null=True)
    seat_availability = serializers.CharField(max_length=30)
    latitude = serializers.DecimalField(
        max_digits=7, decimal_places=5, allow_null=True)
    longitude = serializers.DecimalField(
        max_digits=7, decimal_places=5, allow_null=True)


class StageETAListSerializer(ETASerializer):
    route_id = serializers.CharField(max_length=10)
    bus_type = serializers.CharField(max_length=10)
    location = serializers.CharField(max_length=100)
    destination = serializers.CharField(max_length=100)
    bus_number = serializers.CharField(max_length=10)


class RouteStageETAListSerializer(ETASerializer):
    eta_minutes = serializers.ListField(
        child=serializers.IntegerField(min_value=0)
    )


class VehicleListSerializer(serializers.Serializer):
    vehicle_number = serializers.CharField(max_length=15)
    latitude = serializers.DecimalField(
        max_digits=7, decimal_places=5, allow_null=True)
    longitude = serializers.DecimalField(
        max_digits=7, decimal_places=5, allow_null=True)


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


class StageETASerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='stage_details')
    eta_list = serializers.SerializerMethodField()

    def get_eta_list(self, obj):
        return self.context['eta_list'].data

    class Meta:
        model = Stage
        fields = ('id', 'name', 'name_slug', 'latitude', 'longitude','url', 'eta_list')


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
        fields = ('id', 'name', 'frequency', 'url', 'start_stage','end_stage','stages')

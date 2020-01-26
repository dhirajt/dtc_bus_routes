# -*- coding: utf-8 -*-
from rest_framework import serializers
from busroutes.models import Stage, Route, StageSequence


class ETASerializer(serializers.Serializer):
    seat_availability = serializers.CharField(max_length=30)
    latitude = serializers.DecimalField(
        max_digits=7, decimal_places=5, allow_null=True)
    longitude = serializers.DecimalField(
        max_digits=7, decimal_places=5, allow_null=True)
    location = serializers.CharField(max_length=100)


class StageETAListSerializer(ETASerializer):
    route_id = serializers.CharField(max_length=100)
    bus_type = serializers.CharField(max_length=10)

    destination = serializers.CharField(max_length=100)
    bus_number = serializers.CharField(max_length=10)

    eta_minutes = serializers.IntegerField()
    passengers = serializers.IntegerField(allow_null=True)


class VehicleSerializer(ETASerializer):
    vehicle_number = serializers.CharField(max_length=15)


class StageBasicSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='stage_details')
    class Meta:
        model = Stage
        fields = ('id', 'name', 'url', 'latitude', 'longitude')

class StageAdvancedSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='stage_details')
    bus_count = serializers.IntegerField(source='route_count')
    distance = serializers.SerializerMethodField()
    routes = serializers.SerializerMethodField()

    def get_distance(self, obj):
        if not getattr(obj, 'distance', None):
            return None
        return obj.distance.m

    def get_routes(self, obj):
        if not getattr(obj, 'routes', None):
            return None
        return obj.routes

    class Meta:
        model = Stage
        fields = ('id', 'name', 'name_slug', 'latitude', 'longitude', 'url', 'bus_count', 'distance', 'routes')


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

    stage_count = serializers.IntegerField()

    class Meta:
        model = Route
        fields = ('id', 'name', 'url', 'start_stage','end_stage', 'stage_count')

class RouteAdvancedSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='route_details')
    route_type = serializers.CharField(source='get_route_type_display')

    start_stage = StageBasicSerializer()
    end_stage = StageBasicSerializer()

    stages = StageAdvancedSerializer(many=True)

    class Meta:
        model = Route
        fields = ('id', 'name', 'frequency', 'url', 'route_type', 'start_stage','end_stage','stages')


class RouteAdvancedETASerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='route_details')

    start_stage = StageBasicSerializer()
    end_stage = StageBasicSerializer()

    stages = StageAdvancedSerializer(many=True)

    vehicle_list = serializers.SerializerMethodField()

    def get_vehicle_list(self, obj):
        return self.context['vehicle_list'].data

    class Meta:
        model = Route
        fields = ('id', 'name', 'frequency', 'url', 'start_stage','end_stage','stages', 'vehicle_list')


class NearbyRouteStageSearializer(serializers.Serializer):
    stage = serializers.CharField(max_length=100)
    stage_id = serializers.IntegerField()

    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

    distance = serializers.DecimalField(max_digits=10, decimal_places=3, coerce_to_string=False, allow_null=True)
    bus_count = serializers.IntegerField()

class NearbyRouteSearializer(serializers.Serializer):
    class StageListSerializer(serializers.ListSerializer):
        child = NearbyRouteStageSearializer()

    route = serializers.CharField(max_length=100)
    route_id = serializers.IntegerField()

    start_stage = serializers.CharField(max_length=100)
    end_stage = serializers.CharField(max_length=100)

    route_type = serializers.CharField(max_length=100)
    stage_count = serializers.IntegerField()

    stages = StageListSerializer()

class TripLegSerializer(serializers.Serializer):
    leg_type = serializers.CharField(max_length=100)
    route = RouteBasicSerializer()
    start_stage = StageBasicSerializer()
    end_stage = StageBasicSerializer()
    num_stops = serializers.IntegerField()
    stop_names = serializers.ListField(child=serializers.CharField(max_length=100))

class LegSerializer(serializers.Serializer):
    leg_type = serializers.CharField(max_length=100)
    trip_leg = TripLegSerializer()

class ItinerarySerializer(serializers.Serializer):
    legs = LegSerializer(many=True)

class RoutePlannerSerializer(serializers.Serializer):
    from_stage = StageBasicSerializer()
    to_stage = StageBasicSerializer()

    itineraries = ItinerarySerializer(many=True)

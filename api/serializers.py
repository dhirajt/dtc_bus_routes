# -*- coding: utf-8 -*-
from rest_framework import serializers
from busroutes.models import Stage

class StageBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ('id', 'name')

class StageAdvancedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ('id', 'name', 'name_slug', 'latitude', 'longitude')

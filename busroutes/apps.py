# -*- coding: utf-8 -*-
from django.apps import AppConfig

class BusRoutesConfig(AppConfig):
    name = 'busroutes'

    def ready(self):
        import busroutes.signals
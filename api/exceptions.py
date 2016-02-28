# -*- coding: utf-8 -*-
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['status'] = 'error'
        response.data['message'] = response.data['detail']
        del response.data['detail']
    return response

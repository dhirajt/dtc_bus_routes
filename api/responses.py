# -*- coding: utf-8 -*-
from rest_framework.response import Response

class BusRoutesStandardResponse(Response):
	SUCCESS_STATUS_CODES = [200,304]

	def __init__(self,data,**kwargs):
		super(BusRoutesStandardResponse, self).__init__(data,**kwargs)

		status = kwargs.get('status',200)
		response_status = 'success'

		if status not in self.SUCCESS_STATUS_CODES:
			response_status = 'error'

		self.data = {
			'data': data,
			'status': response_status
		}

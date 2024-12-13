from rest_framework.response import Response
from rest_framework import status

def custom_response(message, status_code, data=None):
    response_data = {
        'message': message,
        'status': status_code,
        'data': data if data is not None else {}
    }
    return Response(response_data, status=status_code)
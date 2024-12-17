from rest_framework.response import Response

def custom_response(message, status_code, data=None):
    response_data = {
        'message': message,
        'status': status_code,
        'data': data if data is not None else {}
    }
    return Response(response_data, status=status_code)

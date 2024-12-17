from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken


def custom_exception_handler(exc, context):
    # Call the default exception handler first
    response = drf_exception_handler(exc, context)
    if isinstance(exc, InvalidToken):
        response.data = {
            "message": "Session is expired or invalid",
            "status": status.HTTP_401_UNAUTHORIZED,
            "data": None
        }
    elif isinstance(exc, PermissionDenied):
        response.data = {
            "message": "You are not authorized to perform this action",
            "status": status.HTTP_403_FORBIDDEN,
            "data": None
        }
    elif isinstance(exc, ValidationError):
        # Handle validation errors
        response.data = {
            "message": "Validation error occurred",
            "status": status.HTTP_400_BAD_REQUEST,
            "data": None
        }

    return response
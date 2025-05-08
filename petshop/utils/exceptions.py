from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound


class CustomNotFound(NotFound):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, error):
        self.detail = {'data': {'error': error}}


class CustomBadRequest(ValidationError):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, error):
        self.detail = {'data': {'error': error}}

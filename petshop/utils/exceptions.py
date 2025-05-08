from rest_framework.exceptions import APIException
from rest_framework import status


class CustomNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, message):
        self.detail = {'data': {'message': message}}

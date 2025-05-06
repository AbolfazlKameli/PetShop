import re

from django.core.exceptions import ValidationError


def validate_iranian_phone_number(value: str):
    pattern = '^(\\+98|0)?9\\d{9}$'

    if not re.match(pattern, value):
        raise ValidationError('Enter a valid iranian phone number.')


def validate_postal_code(value: str):
    pattern = '^\\d{10}$'

    if not re.match(pattern, value):
        raise ValidationError('Enter a valid iranian postal code.')

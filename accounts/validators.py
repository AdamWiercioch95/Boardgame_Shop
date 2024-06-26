from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not value.isdigit() or len(value) != 9:
        raise ValidationError('Phone number must be 9 digits')
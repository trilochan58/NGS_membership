from django.core.exceptions import ValidationError


def validate_phone(value):
    if not value.isdigit():
        raise ValidationError("It should contain only digits.")
    if not value.startswith("9"):
        raise ValidationError("phone number should start with 9.")
    if not len(value)==10:
        raise ValidationError("Phone number should be of 10 digits.")
    
    return value
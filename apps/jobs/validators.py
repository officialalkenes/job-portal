from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_positions(value):
    # Use a regular expression to check if the value contains only characters
    if not value.isalpha():
        raise ValidationError("Positions should only contain characters.")

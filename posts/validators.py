from django.core.exceptions import ValidationError

def validate_email(value):
    email = value
    if ".edu" in email:
        raise ValidationError("we do not accept edu emails")
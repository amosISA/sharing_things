from django.core.exceptions import ValidationError

def validate_title(value):
    title = value
    if title == "amos":
        raise ValidationError('{} {tit}'.format('No puede poner el titulo: ', tit=title))

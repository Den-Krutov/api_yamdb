from django.core.exceptions import ValidationError


def no_me_username_validator(username):
    if username == 'me':
        raise ValidationError('username не может быть me')

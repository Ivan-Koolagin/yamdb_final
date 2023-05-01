import re
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError('Нельзя добавлять произведения из будущего!')
    return value


def validate_username(value):
    if value == settings.NAME_ME:
        raise ValidationError(
            ('Именем не может быть: <me>.'),
            params={'value': value},
        )
    if re.search(r'^[\w.@+-]+\Z', value) is None:
        raise ValidationError(
            ('Использованы недопустимые символы.'),
            params={'value': value},
        )

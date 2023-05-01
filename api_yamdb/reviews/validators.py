from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            ("Год не может быть %(value)s больше текущего!"),
            params={"value": value},
        )

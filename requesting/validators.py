from datetime import date

from django.core.exceptions import ValidationError


def validate_deadline(deadline):
    if deadline < date.today():
        raise ValidationError("Назад в будущее?")

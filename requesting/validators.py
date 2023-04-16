from datetime import date
import re

from django.core.exceptions import ValidationError


PHONE_NUMBER = re.compile(
    r"(\+7)?\s?\(?(2\d{2}|[3-9]\d{2})\)?[\s.-]?\d{3}[\s.-]?\d{4}")


def validate_deadline(deadline):
    if deadline < date.today():
        raise ValidationError("Назад в будущее?")


def validate_phonenumber(number):
    if not PHONE_NUMBER.match(number):
        raise ValidationError(
            "Не правильный формат номера телефона")

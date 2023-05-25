from datetime import date
import re

from django.core.exceptions import ValidationError


PHONE_NUMBER =  re.compile(r'^(\+\d{1,3})? ?(\()?(\d{3})(?(2)\))?[-.\s]?(\d{3})[-.\s]?(\d{2})[-.\s]?(\d{2})$')


def validate_deadline(deadline):
    if deadline < date.today():
        raise ValidationError("Назад в будущее?")


def validate_phonenumber(number):
    if not PHONE_NUMBER.match(number):
        raise ValidationError(
            "Не правильный формат номера телефона")

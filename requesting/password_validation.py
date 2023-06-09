import re

from django.forms import ValidationError

HARD_P = re.compile(
    r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]{4,}).{8,}$"
)


class PasswordValidator:
    def validate(self, password, user):
        if not HARD_P.match(password):
            raise ValidationError("Слабый пароль")

    def get_help_text(self):
        return ""

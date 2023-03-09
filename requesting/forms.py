from collections import defaultdict

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelChoiceField

from django.contrib.auth.models import Group,User


class AddrequestForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ["theme", "requesting_message", "location", "deadline","priority"]
        widgets = {"deadline": forms.DateInput({"type": "date",})}


class RegisterForm(UserCreationForm):

    groups = forms.ModelChoiceField(Group.objects,label="Компания",initial="")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        help_text = defaultdict(
            lambda: "", (("username", "Не менее 6 символов"),)
        )
        for field in self:
            field.help_text = help_text[field.name]

    class Meta(UserCreationForm.Meta):
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

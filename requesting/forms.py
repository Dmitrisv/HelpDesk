from collections import defaultdict

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelChoiceField

from .models import Form, Task, CustomUser, FormMessage
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm


class TaskForm(forms.ModelForm):
    class Task(ModelChoiceField):
        def label_from_instance(self, obj):
            return f"{obj.first_name} {obj.last_name}"

    user = Task(
        CustomUser.objects.filter(is_staff=True, is_superuser=False),
        label="Исполнитель",
        initial="",
        to_field_name="first_name",
    )

    class Meta:
        model = Task
        fields = [
            "user",
            "theme",
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "phone",
            "ip",
        ]


class AddrequestForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = [
            "theme",
            "requesting_message",
            "image",
            "location",
            "deadline",
            "priority",
        ]
        widgets = {
            "deadline": forms.DateInput(
                {
                    "type": "date",
                }
            )
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = FormMessage
        fields = ["message", "image"]


class CustomChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        help_text = defaultdict(lambda: "")
        for field in self:
            field.help_text = help_text[field.name]


class RegisterForm(UserCreationForm):
    groups = forms.ModelChoiceField(Group.objects, label="Компания", initial="")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        help_text = defaultdict(
            lambda: "", (("username", "Не менее 6 символов"),)
        )
        for field in self:
            field.help_text = help_text[field.name]

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]

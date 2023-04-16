from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from . import validators


PRIORITY = (
    ('1', "Нейтрально"),
    ('2', "Средне"),
    ('3', "Срочно"),
)


class CustomUser(AbstractUser, PermissionsMixin):
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    phone  = models.CharField(verbose_name="Номер телефона", validators=[validators.validate_phonenumber],blank=True,max_length=25)
    ip = models.GenericIPAddressField(blank=True,null=True)


class Task(models.Model):
    
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Имя пользователя"
    )
    theme = models.CharField(max_length=50, verbose_name="Тема поручения")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = "Поручение"
        verbose_name_plural = "Поручения"
        permissions = (("can_give_tasks","Может получать задания"),) 


class Form(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Имя пользователя"
    )
    theme = models.CharField(
        max_length=30, verbose_name="Тема", help_text="Уложитесь в 30 символов"
    )
    requesting_message = models.TextField(
        max_length=200, verbose_name="Текст сообщения"
    )
    time = models.DateTimeField(
        auto_now_add=True, verbose_name="Время подачи заявки"
    )
    active = models.BooleanField(default=True, verbose_name="Активные")
    location = models.IntegerField(
        verbose_name="Кабинет", validators=[MinValueValidator(1)]
    )
    state = models.CharField(
        max_length=20, default="Ожидает", verbose_name="Состояние"
    )
    done_at = models.DateTimeField(verbose_name="Когда выполненно",null=True)
    deadline = models.DateField(
        verbose_name="Выполнить до", validators=[validators.validate_deadline]
    )
    priority = models.CharField(max_length=2, verbose_name="Приоритет",choices=PRIORITY,default="Нейтрально")
    implementer = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name="implementor",
        verbose_name="Исполнитель",
        blank=True
    )
    soimplementor = models.ManyToManyField(
        CustomUser, related_name="subimplemetor", verbose_name="Соисполнитель",blank=True
    )

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


    @property
    def actual(self):
        return self.deadline >= date.today()

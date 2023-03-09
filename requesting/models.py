from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from . import validators


PRIORITY = (
    ('1', "Нейтрально"),
    ('2', "Средне"),
    ('3', "Срочно"),
)

class Task(models.Model):
    
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Имя пользователя"
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
        User, on_delete=models.CASCADE, verbose_name="Имя пользователя"
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
    deadline = models.DateField(
        verbose_name="Выполнить до", validators=[validators.validate_deadline]
    )
    priority = models.CharField(max_length=2, verbose_name="Приоритет",choices=PRIORITY,default="Нейтрально")
    implementer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="implementor",
        verbose_name="Исполнитель",
    )
    soimplementor = models.ManyToManyField(
        User, related_name="subimplemetor", verbose_name="Соисполнитель"
    )

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


    @property
    def actual(self):
        return self.deadline >= date.today()

from datetime import date

from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from . import validators
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


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

class FormMessage(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Имя пользователя", 
    )
    message = models.TextField(_("Сообщение"), max_length=200)
    image = models.ImageField(_("Вложение"), null = True, blank = True,)
    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(64, 64)],
                                      format='JPEG',
                                      options={'quality': 60})
    class Meta:
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.message


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
    done_at = models.DateTimeField(verbose_name="Когда выполненно",blank=True,null=True)
    image = models.ImageField(_("Вложение"),blank=True,null=True)
    image_thumbnail = ImageSpecField(source='image',
                                      processors=[ResizeToFill(64, 64)],
                                      format='JPEG',
                                      options={'quality': 60})
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
    messages = models.ManyToManyField(FormMessage, verbose_name=_("Сообщения"),blank=True, null = True)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


    @property
    def actual(self):
        return self.deadline >= date.today()

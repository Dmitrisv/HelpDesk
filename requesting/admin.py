from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models

admin.site.unregister(User)


@admin.register(User)
class Users(BaseUserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
        "last_login",
        "id",
    )



    list_filter = ("username","is_staff","is_superuser","groups",)
    
    actions = ("upgrade", "deactivation","activation")

    @admin.action(description="Повысить до Исполняющего")
    def upgrade(self, request, queryset):
        queryset.update(is_staff=True)

    @admin.action(description="Деактивировать аккаунт(ы)")
    def deactivation(self, request, queryset):
        queryset.update(is_active=False)    
    
    @admin.action(description="Активировать аккаунт(ы)")
    def activation(self, request, queryset):
        queryset.update(is_active=True)


@admin.register(models.Task)
class Tasks(admin.ModelAdmin):
    list_display = ("user","theme")
    list_filter = ("user",)

    


@admin.register(models.Form)
class Requests(admin.ModelAdmin):
    list_filter = ("active", "user", "state", "implementer","time" )
    list_display = ("theme", "id", "deadline", "human_nickname")
    actions = ("recorrect",)


    def human_nickname(self, object):
        return f"{object.user.first_name} {object.user.last_name}"

    human_nickname.short_description = "Подающий заявку"

    @admin.action(description="Отправть на переисполнение")
    def recorrect(self, request, queryset):
        queryset.update(active=True, state="Исправление", implementer=None)

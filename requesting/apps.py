from django.apps import AppConfig


class RequestingConfig(AppConfig):
    name = "requesting"
    verbose_name = "Обработчик заявок"

    def ready(self):
        from . import signals

from django.db.models.signals import post_save

from .consumers import consumers
from .models import Form


def on_request_create(**kwargs):
    for consumer in consumers:
        consumer.receive_json()


post_save.connect(on_request_create, Form)

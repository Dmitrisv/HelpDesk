from django.urls import path

from . import consumers

websocket_urlpatterns = [path("ws/rtm/", consumers.Requests.as_asgi())]

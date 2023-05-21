from django.urls import path,re_path

from . import consumers

websocket_urlpatterns = [path("ws/rtm/", consumers.Requests.as_asgi()),
                        re_path(r'ws/request/(?P<id>\d+)/$', consumers.ChatConsumer.as_asgi()),]

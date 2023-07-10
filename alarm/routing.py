from django.urls import path

from . import consumers

websocket_urlpatterns = [
    # path("ws/alarm/", consumers.AlarmConsumer.as_asgi()),
    path("alarm/", consumers.AlarmConsumer.as_asgi()),
]

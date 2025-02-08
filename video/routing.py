from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # This route passes a room_name parameter to the consumer.
    re_path(r'ws/video/(?P<room_name>\w+)/$', consumers.VideoConsumer.as_asgi()),
]

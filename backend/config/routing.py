from django.urls import re_path
from apps.fitting import consumers

websocket_urlpatterns = [
    re_path(r'ws/vto/status/(?P<try_on_id>\w+)/$', consumers.VTOStatusConsumer.as_asgi()),
]

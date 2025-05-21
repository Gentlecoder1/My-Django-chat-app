from django.urls import re_path
from chatbox import consumers  # You will create this next

websocket_urlpatterns = [
    # Example: ws/chat/room_name/
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

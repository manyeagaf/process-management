from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<conversation_name>.+)/(?P<user_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/notification/(?P<user_id>\w+)/$', consumers.NotificationConsumer.as_asgi()),
    
]

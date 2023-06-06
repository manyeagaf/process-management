from django.urls import path,include

from . import views
from rest_framework import routers
from .api_views import ConversationViewSet,MessageViewSet
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)
urlpatterns = [
    path('', views.index_view, name='chat-index'),
    path('<str:room_id>/', views.room_view, name='chat-room'),
    path('api/',include(router.urls))
]

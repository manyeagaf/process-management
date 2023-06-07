from chat_app.models import Conversation,Message
from chat_app.serializers import MessageSerializer, ConversationSerializer
from rest_framework import viewsets
from users.models import User

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        queryset = Conversation.objects.filter(
            name__contains=self.request.GET.get("user")
        )
        # queryset = Conversation.objects.filter(
        #     name__contains=self.request.user.id
        # )
        return queryset
    def get_serializer_context(self):
        user = User.objects.get(id = self.request.GET.get("user"))
        return {"request": self.request, "user": user}

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
   
from chat_app.models import Message, Conversation
from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("id","email","first_name","last_name")
    
class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ("id", "name","last_message","unread_count","other_user")

    def get_last_message(self, obj):
        messages = obj.messages.all().order_by("-timestamp")
        if not messages.exists():
            return None
        message = messages[0]
        return MessageSerializer(message).data
    def get_other_user(self, obj):
        emails = obj.name.split("__")
        context = {}     
        for email in emails:
            if email != self.context["user"].email:
                # This is the other participant
                other_user = User.objects.get(email=email)   
                return UserSerializer(other_user).data
     
    def get_unread_count(self,obj):
        emails = obj.name.split("__")
        context = {}     
        for email in emails:
            if email != self.context["user"].email:
                # This is the other participant
                other_user = User.objects.get(email=email) 
        return obj.messages.filter(read=False,from_user = other_user).count()

    

class MessageSerializer(serializers.ModelSerializer):
     
#     from_user = serializers.SerializerMethodField()
#     to_user = serializers.SerializerMethodField()
    conversation = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            "id",
            "conversation",
            "from_user",
            "to_user",
            "content",
            "timestamp",
            "read",
            "message_type",
            "image"
        )

    def get_conversation(self, obj):
        return str(obj.conversation.id)

#     def get_from_user(self, obj):
#         return UserSerializer(obj.from_user).data

#     def get_to_user(self, obj):
#         return UserSerializer(obj.to_user).data
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer,WebsocketConsumer
from users.models import User
from django.db.models import Q

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ChatConsumer(WebsocketConsumer):
    """
    This consumer is used to show user's online status,
    and send notifications.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.conversation_name = None
        self.conversation = None

    def connect(self):
        self.user = User.objects.get(pk = self.scope['url_route']['kwargs']['user_id'])
        # if not self.user.is_authenticated:
        #     return

        self.accept()
        self.conversation_name = (
            f"{self.scope['url_route']['kwargs']['conversation_name']}"
        )
        self.conversation, created = Conversation.objects.get_or_create(
            name=self.conversation_name
        )
    #     self.conversation, created = Conversation.objects.filter(
    # Q(name=self.conversation_name) | Q(name=reversed(self.conversation_name))
# ).get_or_create(name=self.conversation_name)

        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name,
        )

        self.send(
            json.dumps(
            {
                "type": "online_user_list",
                "users": [user.email for user in self.conversation.online.all()],
            }
            )
        )

        async_to_sync(self.channel_layer.group_send)(
            self.conversation_name,
            {
                "type": "user_join",
                "user": self.user.email,
            },
        )

        messages = self.conversation.messages.all()
        
        # message_count = self.conversation.messages.all().count()
        self.send(
            json.dumps(
            {
                "type": "last_50_messages",
                "messages": MessageSerializer(messages, many=True).data,
                
            }
            )
        )

        self.conversation.online.add(self.user)

        

    def disconnect(self, code):
        self.user = User.objects.get(pk = self.scope['url_route']['kwargs']['user_id'])
        # if self.user.is_authenticated:
        #     # send the leave event to the room
        #     async_to_sync(self.channel_layer.group_send)(
        #         self.conversation_name,
        #         {
        #             "type": "user_leave",
        #             "user": self.user.email,
        #         },
        #     )
        async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    "type": "user_leave",
                    "user": self.user.email,
                },
            )
        self.conversation.online.remove(self.user)
        return super().disconnect(code)

    def get_receiver(self):
        usernames = self.conversation_name.split("__")
        for username in usernames:
            if username != self.user.id:
                # This is the receiver
                return User.objects.get(pk=username)

    def receive(self, text_data=None, bytes_data=None):
        content = json.loads(text_data)
        message_type = content["type"]
        message = None
        if message_type == "image":
            message = Message.objects.get(pk = content["id"])
            
        else:
            message = Message.objects.create(from_user = User.objects.get(pk = content["from_user"]),to_user = User.objects.get(pk = content["to_user"]),content =content["message"],message_type = content['type'],conversation = self.conversation)
            # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    'type': "chat_message",
                    'message': MessageSerializer(message).data,
                }
            )
         
        notification_group_name = str(self.get_receiver().id) + "__notifications"
        async_to_sync(self.channel_layer.group_send)(
                notification_group_name,
                {
                    "type": "new_message_notification",
                    "name": self.user.username,
                    "message": MessageSerializer(message).data,
                },
            )

    # def chat_message_echo(self, event):
    #     self.send(text_data=json.dumps(event))

    def user_join(self, event):
        self.send(text_data=json.dumps(event))

    def user_leave(self, event):
        self.send(text_data=json.dumps(event))

    # def typing(self, event):
    #     self.send(text_data=json.dumps(event))

    # def new_message_notification(self, event):
    #     self.send(text_data=json.dumps(event))

    # def unread_count(self, event):
    #     self.send(text_data=json.dumps(event))
    def chat_message(self, event):
        self.send(text_data=json.dumps(event))


class NotificationConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.notification_group_name = None

    def connect(self):
        self.user = User.objects.get(pk = self.scope['url_route']['kwargs']['user_id'])
        # if not self.user.is_authenticated:
        #     return

        self.accept()

        # private notification group
        self.notification_group_name = str(self.user.id) + "__notifications"
        async_to_sync(self.channel_layer.group_add)(
            self.notification_group_name,
            self.channel_name,
        )

        # Send count of unread messages and conversations
        conversations = Conversation.objects.filter(name__contains = self.user.id)
        unread_count = Message.objects.filter(to_user=self.user, read=False).count()
        self.send(
            json.dumps(
            {
                "type": "unread_count",
                "unread_count": unread_count,
                "conversations": ConversationSerializer(conversations,many=True,context = {"user":self.user}).data
            })
        )

        # # Send all user conversations
        # conversations = Conversation.objects.filter(name__contains = self.user.id)
        # print(conversations)
        
        # self.send(
        #     json.dumps(
        #     {
        #         "type": "conversations",
        #         "conversations": ConversationSerializer(conversations,many=True,context = {"user":self.user}).data
        #     })
        # )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.notification_group_name,
            self.channel_name,
        )
        return super().disconnect(code)

    def new_message_notification(self, event):
        self.send(json.dumps(event))

    def unread_count(self, event):
        self.send(json.dumps(event))
    def conversations(self, event):
        self.send(json.dumps(event))








# class ChatConsumer(WebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(args, kwargs)
#         self.conversation_name = None
#         self.conversation_group_name = None
#         self.room = None
#         self.user = None

#     def connect(self):
#         self.room_id = self.scope['url_route']['kwargs']['room_id']
#         self.room_group_name = f'chat_{self.room_id}'
#         self.room = Room.objects.get(pk=self.room_id)
#         self.user = User.objects.get(pk = self.scope['url_route']['kwargs']['user_id'])

#         # connection has to be accepted
#         self.accept()

#         # join the room group
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name,
#         )

#          # send the user list to the newly joined user
#         self.send(json.dumps({
#             'type': 'user_list',
#             'users': [user.id for user in self.room.online.all()],
#         }))

#         #Add user to online users
#         self.room.online.add(self.user)
#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name,
#         )
#         #Remove user from online users
#         self.room.online.remove(self.user)

#     def receive(self, text_data=None, bytes_data=None):
#         content_json = json.loads(text_data)
#         message_type = content_json['type']
#         if message_type == "image":
#             message = Message.objects.get(pk = content_json["id"])
#             async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': "chat_message",
#                 'message': MessageSerializer(message).data
#             },
#         )
#         else:
#             message = Message.objects.create(user = User.objects.get(pk = content_json["sender"]),content =content_json["message"],message_type = content_json['type'],room = self.room)
#             # send chat message event to the room
#             async_to_sync(self.channel_layer.group_send)(
#                 self.room_group_name,
#                 {
#                     'type': "chat_message",
#                     'message': MessageSerializer(message).data,
#                 }
#             )
#     def chat_message(self, event):
#         self.send(text_data=json.dumps(event))
    
    
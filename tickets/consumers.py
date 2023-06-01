import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from tickets.models import Comment
class ChatConsumer(WebsocketConsumer):
    # @database_sync_to_async
    # def create_chat(self, msg, sender):
    #     return Comment.objects.create(sender=sender, msg=msg)
        
    def connect(self):

        self.user = self.scope['user']
        
        self.id = self.scope['url_route']['kwargs']['request_id']
        self.room_group_name = 'chat_%s' % self.id
        
        # join room group
        self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name
        )
        
        self.accept()
    def disconnect(self, close_code):
        # leave room group
        self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
        )
    # receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        print(message)
        # send message to room group
        self.channel_layer.group_send(
        self.room_group_name,
        {
        'type': 'chat_message',
        'message': message,
        'user': self.user.username,
        'datetime': now.isoformat(),
        }
        )
    # receive message from room group
    def chat_message(self, event):
    # Send message to WebSocket
        self.send(text_data=json.dumps(event))


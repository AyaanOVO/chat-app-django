from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from .models import Message
import json

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope["user"]
        self.other_user = self.scope['url_route']['kwargs']['username']

        users = sorted([self.user.username, self.other_user])
        self.room_group_name = f"chat_{users[0]}_{users[1]}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        sender = self.user
        receiver = User.objects.get(username=self.other_user)

        Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=message
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
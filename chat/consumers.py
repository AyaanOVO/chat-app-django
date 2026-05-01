from .models import Message
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
import json


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.user1 = self.scope['url_route']['kwargs']['user1']
        self.user2 = self.scope['url_route']['kwargs']['user2']

        users = sorted([self.user1, self.user2])
        self.room_group_name = f"chat_{users[0]}_{users[1]}"

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        messages = Message.objects.filter(
            sender__username__in=[self.user1, self.user2],
            receiver__username__in=[self.user1, self.user2]
        ).order_by('timestamp')

        for msg in messages:
            self.send(text_data=json.dumps({
                'message': msg.content,
                'sender': msg.sender.username
            }))

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        sender = User.objects.get(username=self.user1)
        receiver = User.objects.get(username=self.user2)

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
                'sender': self.user1
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender']
        }))
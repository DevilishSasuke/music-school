import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from main.models import MyUser
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.other_user_username = self.scope['url_route']['kwargs']['username']
    self.other_user = await self.get_user(self.other_user_username)

    if not self.other_user:
      await self.close()
      return
    
    self.user = self.scope['user']
    self.room_name = f'chat_{self.user.username}_{self.other_user.username}'
    self.room_group_name = f'chat_{min(self.user.username, self.other_user.username)}_{max(self.user.username, self.other_user_username)}'  
    
    await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name
    )

    await self.accept()

  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
    )

  async def receive(self, text_data):
    text_data_json = json.loads(text_data)
    message=text_data_json['message']

    await self.save_message(self.user, self.other_user, message)

    await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
                'timestamp': text_data_json['timestamp']
            }
        )
    
  async def chat_message(self, event):
    message = event['message']
    username = event['username']
    timestamp = event['timestamp']

    await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))
    
  @database_sync_to_async
  def get_user(self, username):
        try:
            return MyUser.objects.get(username=username)
        except MyUser.DoesNotExist:
            return None

  @database_sync_to_async
  def save_message(self, sender, receiver, message):
        Message.objects.create(sender=sender, reciever=receiver, message=message)






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

  async def recieve(self, text_data):
    pass


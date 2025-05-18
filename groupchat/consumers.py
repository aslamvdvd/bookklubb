import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async # For database operations
from django.contrib.auth import get_user_model
from discussions.models import DiscussionGroup, GroupMembership
from .models import GroupChatMessage

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_group_name = f'chat_{self.group_id}'
        self.user = self.scope['user']

        if not self.user or not self.user.is_authenticated:
            await self.close()
            return

        # Check if user is a member of the group (database operation)
        is_member = await self.is_user_member(self.user, self.group_id)
        if not is_member:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if hasattr(self, 'room_group_name') and hasattr(self, 'channel_name'):
             await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    # Receive message from WebSocket client
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json.get('message')
        # file_data = text_data_json.get('file') # Handling file uploads via WebSocket is more complex

        if not message_text:
            return

        # Save message to database
        chat_message = await self.save_message(self.user, self.group_id, message_text)
        if not chat_message: # Handle case where message saving failed (e.g. group not found)
            # Optionally send an error back to the client
            return

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message', # Convention: type of event
                'message_id': chat_message.id,
                'user_id': self.user.id,
                'username': self.user.username, # Or get_full_name()
                'user_full_name': await self.get_user_full_name(self.user),
                'text': chat_message.text_content,
                'timestamp': chat_message.timestamp.isoformat(),
                # 'file_url': chat_message.file_attachment.url if chat_message.file_attachment else None,
                # 'file_name': chat_message.file_attachment.name.split('/')[-1] if chat_message.file_attachment else None,
            }
        )

    # Handler for messages broadcasted to the room group (e.g., from receive method)
    async def chat_message(self, event):
        # Send message data to WebSocket client
        await self.send(text_data=json.dumps({
            'id': event['message_id'],
            'user_id': event['user_id'],
            'username': event['username'],
            'user_full_name': event['user_full_name'],
            'text': event['text'],
            'timestamp': event['timestamp'],
            # 'file_url': event['file_url'],
            # 'file_name': event['file_name'],
        }))

    @database_sync_to_async
    def is_user_member(self, user, group_id):
        try:
            group = DiscussionGroup.objects.get(id=group_id)
            return GroupMembership.objects.filter(user=user, group=group).exists()
        except DiscussionGroup.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, user, group_id, message_text):
        try:
            group = DiscussionGroup.objects.get(id=group_id)
            # For now, only text messages via WebSocket. File uploads are more complex here.
            chat_message = GroupChatMessage.objects.create(
                user=user,
                group=group,
                text_content=message_text
            )
            return chat_message
        except DiscussionGroup.DoesNotExist:
            # Handle error, maybe log or raise an exception that the consumer can catch
            return None 
        
    @database_sync_to_async
    def get_user_full_name(self, user):
        return user.get_full_name() or user.username 
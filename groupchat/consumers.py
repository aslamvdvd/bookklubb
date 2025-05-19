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
        temp_id = text_data_json.get('temp_id') # Get temp_id from client

        if not message_text:
            # Optionally send an error if message is empty but temp_id was provided
            return

        # Save message to database
        chat_message = await self.save_message(self.user, self.group_id, message_text)
        if not chat_message:
            # Handle message saving failure - potentially send error back to client using temp_id
            if temp_id:
                await self.send(text_data=json.dumps({
                    'type': 'message.error',
                    'temp_id': temp_id,
                    'error': 'Message could not be saved.'
                }))
            return

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message', 
                'message_id': chat_message.id,
                'temp_id': temp_id, # Include temp_id in broadcast
                'user_id': self.user.id,
                'username': self.user.username,
                'user_full_name': await self.get_user_full_name(self.user),
                'text': chat_message.text_content,
                'timestamp': chat_message.timestamp.isoformat(),
            }
        )

    # Handler for messages broadcasted to the room group (e.g., from receive method)
    async def chat_message(self, event):
        # This method sends the broadcasted message to the client
        await self.send(text_data=json.dumps({
            'id': event['message_id'],
            'temp_id': event.get('temp_id'), # Include temp_id if present
            'user_id': event['user_id'],
            'username': event['username'],
            'user_full_name': event['user_full_name'],
            'text': event['text'],
            'timestamp': event['timestamp'],
            # Indicate this is a standard message broadcast
            'message_type': 'new_message' 
        }))

    # Future: Handler for specific message error events if needed
    # async def message_error(self, event):
    #     await self.send(text_data=json.dumps({
    #         'type': 'message.error',
    #         'temp_id': event['temp_id'],
    #         'error': event['error'],
    #     }))

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
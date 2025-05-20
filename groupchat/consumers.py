import json
import logging # Import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async # For database operations
from django.contrib.auth import get_user_model
from discussions.models import DiscussionGroup, GroupMembership
from .models import GroupChatMessage

User = get_user_model()
logger = logging.getLogger(__name__) # Get a logger instance

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_group_name = f'chat_{self.group_id}'
        self.user = self.scope['user']
        logger.info(f"Connect Step 1: User {self.user} attempting to connect to group {self.group_id}.") # Reverted to INFO
        logger.error(f"ERROR_LOG: Connect Step 1: User {self.user}, Group {self.group_id}")

        if not self.user or not self.user.is_authenticated:
            logger.warning(f"User {self.user} is not authenticated. Closing connection to group {self.group_id}.")
            logger.error(f"ERROR_LOG: Connect Step 2a - Not authenticated. Closing. User {self.user}, Group {self.group_id}")
            await self.close()
            return
        logger.error(f"ERROR_LOG: Connect Step 2b - Authenticated. User {self.user}, Group {self.group_id}")

        is_member = await self.is_user_member(self.user, self.group_id)
        logger.error(f"ERROR_LOG: Connect Step 3 - is_member call returned: {is_member}. User {self.user}, Group {self.group_id}")
        if not is_member:
            logger.warning(f"User {self.user} is not a member of group {self.group_id}. Closing connection.")
            logger.error(f"ERROR_LOG: Connect Step 4a - Not member. Closing. User {self.user}, Group {self.group_id}")
            await self.close()
            return
        logger.error(f"ERROR_LOG: Connect Step 4b - Is member. User {self.user}, Group {self.group_id}")

        logger.info(f"User {self.user} successfully connected to group {self.group_id}. Adding to channel layer.")
        logger.error(f"ERROR_LOG: Connect Step 5 - Before group_add. User {self.user}, Group {self.group_id}")
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        logger.error(f"ERROR_LOG: Connect Step 6 - After group_add, before accept. User {self.user}, Group {self.group_id}")
        await self.accept()
        logger.info(f"WebSocket accepted for user {self.user} in group {self.group_id}.")
        logger.error(f"ERROR_LOG: Connect Step 7 - After accept. User {self.user}, Group {self.group_id}")

    async def disconnect(self, close_code):
        logger.error(f"ERROR_LOG: Disconnect called. User {self.user}, Group {self.group_id}, Code: {close_code}") # Add error log here
        logger.info(f"User {self.user} disconnecting from group {self.group_id} with code: {close_code}")
        if hasattr(self, 'room_group_name') and hasattr(self, 'channel_name'):
             await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        logger.info(f"User {self.user} removed from channel layer for group {self.group_id}.")

    async def receive(self, text_data):
        logger.info(f"Received message from user {self.user} in group {self.group_id}: {text_data}")
        try:
            text_data_json = json.loads(text_data)
            message_text = text_data_json.get('message')
            temp_id = text_data_json.get('temp_id') 

            if not message_text:
                logger.warning(f"Received empty message text from {self.user} (temp_id: {temp_id}). Ignoring.")
                return

            logger.info(f"Attempting to save message for user {self.user}, group {self.group_id}, temp_id {temp_id}.")
            chat_message = await self.save_message(self.user, self.group_id, message_text)
            
            if not chat_message:
                logger.error(f"Failed to save message for user {self.user}, group {self.group_id}, temp_id {temp_id}.")
                if temp_id:
                    await self.send(text_data=json.dumps({
                        'type': 'message.error',
                        'temp_id': temp_id,
                        'error': 'Message could not be saved due to a server issue.'
                    }))
                return
            
            logger.info(f"Message saved (ID: {chat_message.id}) for user {self.user}. Broadcasting to group {self.group_id}.")
            user_full_name = await self.get_user_full_name(self.user)
            logger.info(f"Retrieved full name '{user_full_name}' for user {self.user}.")

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat.message',
                    'message_id': chat_message.id,
                    'temp_id': temp_id, 
                    'user_id': self.user.id,
                    'username': self.user.username,
                    'user_full_name': user_full_name,
                    'text': chat_message.text_content,
                    'timestamp': chat_message.timestamp.isoformat(),
                }
            )
            logger.info(f"Message (ID: {chat_message.id}, temp_id: {temp_id}) broadcasted to group {self.room_group_name}.")
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError in receive for user {self.user}, group {self.group_id}: {e}. Data: {text_data}")
        except Exception as e:
            logger.error(f"Generic Exception in receive for user {self.user}, group {self.group_id}: {e}", exc_info=True) # Log full traceback
            # Optionally, send a generic error to the client if a temp_id was available
            if locals().get('temp_id'):
                 await self.send(text_data=json.dumps({
                    'type': 'message.error',
                    'temp_id': locals().get('temp_id'),
                    'error': 'An unexpected server error occurred.'
                }))

    async def chat_message(self, event):
        logger.info(f"Sending chat_message event to client {self.channel_name} in group {self.group_id}: {event}")
        await self.send(text_data=json.dumps({
            'id': event['message_id'],
            'temp_id': event.get('temp_id'), 
            'user_id': event['user_id'],
            'username': event['username'],
            'user_full_name': event['user_full_name'],
            'text': event['text'],
            'timestamp': event['timestamp'],
            'message_type': 'new_message' 
        }))
        logger.info(f"chat_message event sent to client {self.channel_name}.")

    # Future: Handler for specific message error events if needed
    # async def message_error(self, event):
    #     await self.send(text_data=json.dumps({
    #         'type': 'message.error',
    #         'temp_id': event['temp_id'],
    #         'error': event['error'],
    #     }))

    @database_sync_to_async
    def is_user_member(self, user, group_id):
        logger.info(f"Checking membership for user {user.id} in group {group_id}")
        try:
            group = DiscussionGroup.objects.get(id=group_id)
            is_member = GroupMembership.objects.filter(user=user, group=group).exists()
            logger.info(f"User {user.id} membership status in group {group_id}: {is_member}")
            return is_member
        except DiscussionGroup.DoesNotExist:
            logger.error(f"DiscussionGroup with id {group_id} DoesNotExist in is_user_member for user {user.id}.")
            return False
        except Exception as e:
            logger.error(f"Exception in is_user_member for user {user.id}, group {group_id}: {e}", exc_info=True)
            return False # Important to return a boolean

    @database_sync_to_async
    def save_message(self, user, group_id, message_text):
        logger.info(f"DB: Attempting to save message by user {user.id} in group {group_id}: '{message_text[:50]}...'")
        try:
            group = DiscussionGroup.objects.get(id=group_id)
            chat_message = GroupChatMessage.objects.create(
                user=user,
                group=group,
                text_content=message_text
            )
            logger.info(f"DB: Message saved with ID {chat_message.id} by user {user.id} in group {group_id}.")
            return chat_message
        except DiscussionGroup.DoesNotExist:
            logger.error(f"DB: DiscussionGroup {group_id} DoesNotExist in save_message for user {user.id}.")
            return None 
        except Exception as e:
            logger.error(f"DB: Exception in save_message for user {user.id}, group {group_id}: {e}", exc_info=True)
            return None
        
    @database_sync_to_async
    def get_user_full_name(self, user):
        logger.info(f"DB: Getting full name for user {user.id}")
        try:
            name = user.get_full_name() or user.username
            logger.info(f"DB: Retrieved name '{name}' for user {user.id}")
            return name
        except Exception as e:
            logger.error(f"DB: Exception in get_user_full_name for user {user.id}: {e}", exc_info=True)
            return user.username # Fallback 
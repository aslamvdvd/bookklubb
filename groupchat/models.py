"""
Models for the group chat application.

This module defines the data structures used for storing and managing
real-time chat messages within discussion groups.
"""
from django.conf import settings
from django.db import models
from discussions.models import DiscussionGroup # Assuming DiscussionGroup is in discussions.models

class GroupChatMessage(models.Model):
    """
    Represents a single message within a discussion group's chat.
    
    Attributes:
        group (ForeignKey): The discussion group this message belongs to.
        user (ForeignKey): The user who sent this message.
        text_content (TextField): The textual content of the message. Can be empty if it's a file-only message.
        file_attachment (FileField): An optional file attached to the message.
        timestamp (DateTimeField): The date and time when the message was created.
    """
    group = models.ForeignKey(
        DiscussionGroup, 
        on_delete=models.CASCADE, 
        related_name='chat_messages',
        help_text="The discussion group this message belongs to."
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="The user who sent this message."
    )
    text_content = models.TextField(
        blank=True, 
        null=True,
        help_text="The textual content of the message."
    )
    file_attachment = models.FileField(
        upload_to='group_chat_files/%Y/%m/%d/', 
        blank=True, 
        null=True,
        help_text="An optional file attached to the message."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the message was created."
    )

    def __str__(self):
        """String representation of a chat message, showing the user, group, and a snippet of the content."""
        content_type = "File" if self.file_attachment and not self.text_content else "Text"
        snippet = str(self.text_content)[:30] + '...' if self.text_content and len(str(self.text_content)) > 30 else self.text_content
        if self.file_attachment and self.text_content:
            content_description = f"Text & File: {snippet}"
        elif self.file_attachment:
            content_description = f"File: {self.file_attachment.name.split('/')[-1]}"
        else:
            content_description = f"Text: {snippet}"
        
        return f"{self.user.username} in {self.group.name} ({content_description}) at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['timestamp'] # Order messages by when they were sent
        verbose_name = "Group Chat Message"
        verbose_name_plural = "Group Chat Messages"

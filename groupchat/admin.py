"""
Admin configurations for the group chat application.

This module defines how models from the group chat app, such as
GroupChatMessage, are displayed and managed in the Django admin interface.
"""
from django.contrib import admin
from .models import GroupChatMessage

@admin.register(GroupChatMessage)
class GroupChatMessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the GroupChatMessage model.
    
    Displays group, user, a snippet of text_content, file_attachment, and timestamp.
    Provides search functionality by text_content and filtering by group and user.
    """
    list_display = ('group', 'user', 'text_content_snippet', 'file_attachment', 'timestamp')
    list_filter = ('group', 'user', 'timestamp')
    search_fields = ('text_content', 'user__username', 'group__name')
    readonly_fields = ('timestamp',)

    def text_content_snippet(self, obj):
        """Returns a snippet of the text content for display in the admin list."""
        if obj.text_content:
            return (obj.text_content[:50] + '...') if len(obj.text_content) > 50 else obj.text_content
        return "N/A"
    text_content_snippet.short_description = 'Text Snippet'

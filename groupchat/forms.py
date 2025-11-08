"""
Forms for the group chat application.

This module defines forms used for creating and validating
chat messages within discussion groups.
"""
from django import forms
from .models import GroupChatMessage

class MessageForm(forms.ModelForm):
    """
    Form for creating a new GroupChatMessage.
    Handles text content and file attachments.
    """
    text_content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Type your message...',
                'class': 'flex-grow p-3 border-2 border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 resize-none',
                'rows': '1' # Start with one row, JS will auto-resize
            }
        ),
        required=False # Allow file-only messages
    )
    file_attachment = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'hidden', # Actual input is hidden, triggered by a styled label
                'id': 'file_attachment_input' # Match ID used in template for label association
            }
        ),
        required=False # Allow text-only messages
    )

    class Meta:
        model = GroupChatMessage
        fields = ['text_content', 'file_attachment']

    def clean(self):
        """Ensure that at least text or a file is provided."""
        cleaned_data = super().clean()
        text = cleaned_data.get('text_content')
        file = cleaned_data.get('file_attachment')

        if not text and not file:
            raise forms.ValidationError("You must provide either text or a file for your message.")
        
        return cleaned_data 
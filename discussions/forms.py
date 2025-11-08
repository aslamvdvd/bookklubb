from django import forms
from .models import DiscussionGroup
from content.models import ContentItem # Assuming ContentItem is the model name

class DiscussionGroupForm(forms.ModelForm):
    """Form for creating a new DiscussionGroup."""
    name = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Enter group name (e.g., "Sci-Fi Book Club")'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500',
            'rows': 4,
            'placeholder': 'Describe your group (optional)'
        }),
        required=False
    )
    content_item = forms.ModelChoiceField(
        queryset=ContentItem.objects.all(), # Or a more filtered queryset
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500'
        }),
        help_text="Select the content item this group will be primarily focused on.",
        label="Focus Content Item"
    )
    is_private = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'h-5 w-5 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500'
        }),
        label="Make this group private?"
    )

    class Meta:
        model = DiscussionGroup
        fields = ['name', 'description', 'content_item', 'is_private'] 
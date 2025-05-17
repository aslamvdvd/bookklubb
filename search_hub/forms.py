from django import forms
from content.models import ContentItem # To get content types

# Dynamically generate choices for content item types
# This will only work if all apps are loaded when this form is defined.
CONTENT_TYPE_CHOICES = [('', 'Any Content Type')]
try:
    # This approach gets a list of concrete subclasses of ContentItem
    # It relies on apps being loaded. If this form is imported too early, it might be empty.
    concrete_models = [model for model in ContentItem.__subclasses__() if not model._meta.abstract]
    CONTENT_TYPE_CHOICES.extend([
        (model._meta.model_name, model._meta.verbose_name_plural.capitalize()) 
        for model in concrete_models
    ])
except Exception: # Broad exception if apps aren't ready
    # Fallback or log an error if needed - for now, it will just have 'Any'
    pass 


class DiscussionSearchForm(forms.Form):
    """Form for searching discussion groups with filtering and ordering."""
    query = forms.CharField(
        label='Search terms',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 text-gray-700 border-2 border-gray-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Group name, creator, focus...'
        })
    )

    is_private = forms.ChoiceField(
        label='Privacy',
        choices=[
            ('', 'Any Privacy'),
            ('false', 'Public Groups'),
            ('true', 'Private Groups'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'text-gray-700 border-gray-300 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )

    # For content_item_type, we can use ContentType framework or hardcode if simpler
    # Using dynamically generated choices based on ContentItem subclasses
    content_type = forms.ChoiceField(
        label='Focus Content Type',
        choices=CONTENT_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'text-gray-700 border-gray-300 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )

    ordering = forms.ChoiceField(
        label='Order by',
        choices=[
            ('-created_at', 'Newest First'),
            ('created_at', 'Oldest First'),
            ('name', 'Name (A-Z)'),
            ('-name', 'Name (Z-A)'),
            # Add more ordering options like member count if desired
            # ('-members_count', 'Most Members'), # Requires annotation
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'text-gray-700 border-gray-300 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'
        })
    )

    # Future filter fields can be added here (e.g., privacy, content type) 
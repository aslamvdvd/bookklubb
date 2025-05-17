from django import forms

class DiscussionSearchForm(forms.Form):
    """Form for searching discussion groups."""
    query = forms.CharField(
        label='Search for Discussion Groups',
        max_length=200,
        required=False, # Allow empty submission to potentially show all or a default set
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 text-gray-700 border-2 border-indigo-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Search by group name, creator, focus...'
        })
    )
    # Future filter fields can be added here (e.g., privacy, content type) 
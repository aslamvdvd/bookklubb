from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    middle_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'middle_name', 'last_name', 'date_of_birth', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.middle_name = self.cleaned_data["middle_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.date_of_birth = self.cleaned_data["date_of_birth"]
        user.email = self.cleaned_data.get("email") # Use .get for optional email
        if commit:
            user.save()
        return user

class UserProfileEditForm(forms.ModelForm):
    # Fields to be edited
    first_name = forms.CharField(max_length=50, required=False, help_text="Optional. Your given name.")
    middle_name = forms.CharField(max_length=50, required=False, help_text="Optional. Your middle name.")
    last_name = forms.CharField(max_length=50, required=False, help_text="Optional. Your family name.")
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us a bit about yourself...'}), required=False)

    # Email and date_of_birth are removed from here as they are not editable

    class Meta:
        model = CustomUser
        # Updated fields list to only include editable fields
        fields = ['first_name', 'middle_name', 'last_name', 'bio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Help text is now directly on field definitions or can be set here if preferred for all.
        # self.fields['first_name'].help_text = "Optional. Your given name." # Moved to field def
        # self.fields['last_name'].help_text = "Optional. Your family name." # Moved to field def
        # Email help text removed as email field is removed
        if 'middle_name' in self.fields: # Adding help text for middle_name if it wasn't on field def
             self.fields['middle_name'].help_text = self.fields['middle_name'].help_text or "Optional. Your middle name." 
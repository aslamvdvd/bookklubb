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
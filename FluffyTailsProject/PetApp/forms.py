from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }
        # Remove help_text and error messages
        help_texts = {
            'username': None,
            'email': None,
        }
        error_messages = {
            'username': {'required': 'Please enter your username.'},
            'email': {'required': 'Please enter your email address.'},
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        help_texts = {
            'image': None,
        }
        error_messages = {
            'image': {'required': 'Please upload an image.'},
        }


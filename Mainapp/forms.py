from .models import Post
from .models import ReplyPost  # Import your ReplyPost model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Add other fields as needed
        
class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        # You can include other fields from your Post model as needed

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        # Add any additional customization for your form fields here if needed


class AccountSettingsForm(UserChangeForm):
    class Meta:
        model = User  # Assuming you have imported User from django.contrib.auth.models
        fields = ['username', 'email', 'first_name', 'last_name']


class ReplyPostForm(forms.ModelForm):
    class Meta:
        model = ReplyPost
        fields = ['content']  # Add other fields as needed



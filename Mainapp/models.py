# mainapp/models.py

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager

class CustomUser(AbstractUser):
    # Additional fields for the custom user model
    full_name = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    profession = models.CharField(max_length=100, blank=True)

    # Resolve clashes in reverse accessors
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        related_query_name='custom_user',
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        related_query_name='custom_user',
        blank=True,
    )

    def __str__(self):
        return self.username

class ReplyPost(models.Model):
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='replies')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply by {self.author.username} on {self.post.title}'

    def get_absolute_url(self):
        # Example: Assuming you have a view named 'view_post' for displaying a post
        return reverse('view_post', args=[str(self.post.id)])
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Example: Assuming you have a view named 'view_post' for displaying a post
        return reverse('view_post', args=[str(self.id)])
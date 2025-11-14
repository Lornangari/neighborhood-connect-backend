from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings
from django.contrib.auth import get_user_model


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')  
    email = models.EmailField(unique=True)
    neighborhood = models.ForeignKey(
        'Neighborhood', on_delete=models.SET_NULL, null=True, blank=True, related_name='residents'
    )

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Neighborhood(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


#announcements model
class Announcement(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


# help-exchange model
class HelpPost(models.Model):
    HELP_TYPE_CHOICES = (
        ('ask', 'Ask for Help'),
        ('offer', 'Offer Help'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="help_posts"
    )
    type = models.CharField(max_length=10, choices=HELP_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.title}"


class Reply(models.Model):
    post = models.ForeignKey(
        HelpPost,
        on_delete=models.CASCADE,
        related_name="replies"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="help_replies"
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.post.title}"


# business
class Business(models.Model):
    CATEGORY_CHOICES = [
        ("restaurant", "Restaurant"),
        ("retail", "Retail"),
        ("service", "Service"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="other")
    image = models.ImageField(upload_to="business_images/", blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# events

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to="event_images/", blank=True, null=True)

    def __str__(self):
        return self.title


# Anonymousposts

from django.db import models
from django.conf import settings
from django.utils import timezone

class AnonymousPost(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to="anonymous_posts/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name="liked_anonymous_posts", 
        blank=True
    )

    def __str__(self):
        return f"Post {self.id} - {self.text[:20]}"

class AnonymousComment(models.Model):
    post = models.ForeignKey(AnonymousPost, related_name="comments", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} on Post {self.post.id}"



# posts model
#from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Unknown User'}: {self.message[:20]}"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"








    

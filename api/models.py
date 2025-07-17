from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings
from django.contrib.auth import get_user_model


class User(AbstractUser):
    email = models.EmailField(unique=True)
    neighborhood = models.ForeignKey(
        'Neighborhood', on_delete=models.SET_NULL, null=True, blank=True, related_name='residents'
    )

class Neighborhood(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.author.username}"


class AnonymousPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='anonymous_posts')
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='anonymous_posts')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AnonymousPost in {self.neighborhood.name} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class HelpExchange(models.Model):
    EXCHANGE_TYPE_CHOICES = [
        ('offer', 'Offer'),
        ('request', 'Request'),
    ]

    CATEGORY_CHOICES = [
        ('tutoring', 'Tutoring'),
        ('repairs', 'Repairs'),
        ('childcare', 'Childcare'),
        ('moving', 'Moving Help'),
        ('tech', 'Tech Support'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exchanges')
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='exchanges')
    type = models.CharField(max_length=10, choices=EXCHANGE_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    contact_info = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.title} by {self.user.username}"



User = get_user_model()

class Business(models.Model):
    name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    contact_info = models.TextField()
    neighborhood = models.ForeignKey('Neighborhood', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='saved_businesses', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.liked_by.count()

    def __str__(self):
        return self.name

    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.post.title}"
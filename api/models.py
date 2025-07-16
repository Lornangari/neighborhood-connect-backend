from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

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

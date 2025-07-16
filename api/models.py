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

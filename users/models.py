from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=255)
    expires_in = models.IntegerField(default=0)
    expires_at = models.DateTimeField(blank=True, null=True)
    scope = models.CharField(max_length=255)

    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255,  blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    password = None

    active_session = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.expires_at = timezone.now() + timedelta(seconds=self.expires_in)
        self.save()
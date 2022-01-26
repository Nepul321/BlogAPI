import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from users.models import UserKey
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        UserKey.objects.create(
            user=instance,
            key=uuid.uuid4()
        )
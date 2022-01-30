from email.policy import default
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class UserKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activated = models.BooleanField(default=False)
    key = models.CharField(max_length=255, default='')


class PasswordResetEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activated = models.BooleanField(default=False)
    key = models.CharField(max_length=255, default="")
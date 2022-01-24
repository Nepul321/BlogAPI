from email.policy import default
from statistics import mode
from django.db import models
from base.models import User

class UserKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activated = models.BooleanField(default=False)
    key = models.CharField(max_length=255, default='')
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)
    datetime = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)

    class Meta:
        ordering = ['-datetime']
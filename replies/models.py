from base.models import User
from django.db import models
from comments.models import Comment

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="reply_likes")
    date = models.DateField(auto_now_add=True)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-datetime']
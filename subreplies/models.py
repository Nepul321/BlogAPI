from base.models import User
from django.db import models
from replies.models import Reply

class SubReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="subreply_likes")
    date = models.DateField(auto_now_add=True)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-datetime']
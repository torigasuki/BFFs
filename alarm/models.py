from django.db import models

from user.models import User
from feed.models import Feed


class Alarm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
